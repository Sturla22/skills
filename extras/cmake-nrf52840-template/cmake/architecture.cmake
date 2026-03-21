include_guard(GLOBAL)

set_property(GLOBAL PROPERTY FW_REGISTERED_TARGETS "")

function(fw_register_target target_name layer_name)
  if(NOT TARGET ${target_name})
    message(FATAL_ERROR "fw_register_target: unknown target `${target_name}`")
  endif()

  set(known_layers contracts domain platform app test)
  list(FIND known_layers "${layer_name}" layer_index)
  if(layer_index EQUAL -1)
    message(
      FATAL_ERROR
      "fw_register_target: unknown layer `${layer_name}` for target `${target_name}`"
    )
  endif()

  set_property(TARGET ${target_name} PROPERTY FW_LAYER "${layer_name}")
  set_property(GLOBAL APPEND PROPERTY FW_REGISTERED_TARGETS "${target_name}")
endfunction()

function(fw_allowed_layers out_var layer_name)
  if(layer_name STREQUAL "contracts")
    set(result "")
  elseif(layer_name STREQUAL "domain")
    set(result "contracts")
  elseif(layer_name STREQUAL "platform")
    set(result "contracts")
  elseif(layer_name STREQUAL "app")
    set(result "contracts;domain;platform")
  elseif(layer_name STREQUAL "test")
    set(result "contracts;domain;platform;app")
  else()
    message(FATAL_ERROR "fw_allowed_layers: unsupported layer `${layer_name}`")
  endif()

  set(${out_var} "${result}" PARENT_SCOPE)
endfunction()

function(fw_collect_target_deps out_var target_name)
  get_target_property(private_links ${target_name} LINK_LIBRARIES)
  get_target_property(interface_links ${target_name} INTERFACE_LINK_LIBRARIES)

  set(all_links ${private_links} ${interface_links})
  set(filtered_links "")

  foreach(link_item IN LISTS all_links)
    if(NOT link_item OR link_item MATCHES "-NOTFOUND$")
      continue()
    endif()

    if(link_item MATCHES "^\\$<")
      continue()
    endif()

    list(APPEND filtered_links "${link_item}")
  endforeach()

  set(${out_var} "${filtered_links}" PARENT_SCOPE)
endfunction()

function(fw_enforce_architecture)
  get_property(registered GLOBAL PROPERTY FW_REGISTERED_TARGETS)
  list(REMOVE_DUPLICATES registered)

  set(violations "")

  foreach(target_name IN LISTS registered)
    get_target_property(target_layer ${target_name} FW_LAYER)
    if(NOT target_layer OR target_layer MATCHES "-NOTFOUND$")
      continue()
    endif()

    fw_allowed_layers(allowed_layers "${target_layer}")
    fw_collect_target_deps(target_deps "${target_name}")

    foreach(dep_name IN LISTS target_deps)
      if(NOT TARGET ${dep_name})
        continue()
      endif()

      get_target_property(dep_layer ${dep_name} FW_LAYER)
      if(NOT dep_layer OR dep_layer MATCHES "-NOTFOUND$")
        continue()
      endif()

      list(FIND allowed_layers "${dep_layer}" allowed_index)
      if(allowed_index EQUAL -1)
        list(APPEND violations
          "${target_name} (${target_layer}) -> ${dep_name} (${dep_layer})"
        )
      endif()
    endforeach()
  endforeach()

  if(violations)
    list(JOIN violations "\n  - " rendered)
    message(
      FATAL_ERROR
      "Architecture enforcement failed.\n"
      "Disallowed dependencies:\n"
      "  - ${rendered}\n"
      "Update cmake/architecture.cmake if the layer policy intentionally changed."
    )
  endif()
endfunction()
