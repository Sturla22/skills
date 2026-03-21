cmake_minimum_required(VERSION 3.25)

project(cmake_nrf52840_template LANGUAGES C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

include(CTest)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(architecture)

option(TEMPLATE_BUILD_FIRMWARE "Build the nRF52840 firmware image." ${CMAKE_CROSSCOMPILING})
option(TEMPLATE_BUILD_HOST_TESTS "Build host-side verification tests." ${BUILD_TESTING})
option(TEMPLATE_ENABLE_SEMIHOSTING "Link the firmware with newlib semihosting support." ON)

function(starter_enable_warnings target_name)
  if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(${target_name} PRIVATE -Wall -Wextra -Wpedantic -Werror)
  endif()
endfunction()

add_library(starter_contracts INTERFACE)
target_include_directories(
  starter_contracts
  INTERFACE
    "${CMAKE_CURRENT_SOURCE_DIR}/libs/contracts/include"
)
fw_register_target(starter_contracts contracts)

add_library(starter_domain STATIC
  libs/domain/src/hello_service.cpp
)
target_include_directories(
  starter_domain
  PUBLIC
    "${CMAKE_CURRENT_SOURCE_DIR}/libs/domain/include"
)
target_link_libraries(starter_domain PUBLIC starter_contracts)
starter_enable_warnings(starter_domain)
fw_register_target(starter_domain domain)

add_library(starter_platform STATIC
  libs/platform/src/semihost_console.cpp
)
target_include_directories(
  starter_platform
  PUBLIC
    "${CMAKE_CURRENT_SOURCE_DIR}/libs/platform/include"
)
target_link_libraries(starter_platform PUBLIC starter_contracts)
starter_enable_warnings(starter_platform)
fw_register_target(starter_platform platform)

if(TEMPLATE_BUILD_FIRMWARE)
  add_executable(hello_nrf52840
    src/main.cpp
    src/startup_nrf52840.c
  )
  target_link_libraries(hello_nrf52840 PRIVATE starter_domain starter_platform)
  target_compile_definitions(hello_nrf52840 PRIVATE STARTER_TARGET_NRF52840=1)
  starter_enable_warnings(hello_nrf52840)
  fw_register_target(hello_nrf52840 app)

  if(CMAKE_CROSSCOMPILING)
    target_link_options(
      hello_nrf52840
      PRIVATE
        "-T${CMAKE_CURRENT_SOURCE_DIR}/ld/nrf52840.ld"
        "-Wl,-Map=${CMAKE_CURRENT_BINARY_DIR}/hello_nrf52840.map"
        "-Wl,--gc-sections"
        "-nostartfiles"
    )

    if(TEMPLATE_ENABLE_SEMIHOSTING)
      target_compile_definitions(
        starter_platform
        PUBLIC
          STARTER_ENABLE_SEMIHOSTING=1
      )
      target_compile_definitions(hello_nrf52840 PRIVATE STARTER_ENABLE_SEMIHOSTING=1)
      target_link_options(
        hello_nrf52840
        PRIVATE
          "--specs=nano.specs"
          "--specs=rdimon.specs"
      )
    endif()

    if(DEFINED CMAKE_OBJCOPY)
      add_custom_command(
        TARGET hello_nrf52840
        POST_BUILD
        COMMAND ${CMAKE_OBJCOPY} -O binary
          $<TARGET_FILE:hello_nrf52840>
          ${CMAKE_CURRENT_BINARY_DIR}/hello_nrf52840.bin
        COMMAND ${CMAKE_OBJCOPY} -O ihex
          $<TARGET_FILE:hello_nrf52840>
          ${CMAKE_CURRENT_BINARY_DIR}/hello_nrf52840.hex
        VERBATIM
      )
    endif()

    if(DEFINED CMAKE_SIZE)
      add_custom_command(
        TARGET hello_nrf52840
        POST_BUILD
        COMMAND ${CMAKE_SIZE} $<TARGET_FILE:hello_nrf52840>
        VERBATIM
      )
    endif()
  endif()
endif()

if(TEMPLATE_BUILD_HOST_TESTS)
  add_executable(hello_service_test
    tests/host/hello_service_test.cpp
  )
  target_link_libraries(hello_service_test PRIVATE starter_domain)
  starter_enable_warnings(hello_service_test)
  fw_register_target(hello_service_test test)

  add_test(NAME hello_service_test COMMAND hello_service_test)

  add_test(
    NAME architecture_violation_rejected
    COMMAND ${CMAKE_COMMAND}
      -S ${CMAKE_CURRENT_SOURCE_DIR}/tests/architecture/invalid-domain-dep
      -B ${CMAKE_CURRENT_BINARY_DIR}/tests/architecture/invalid-domain-dep
  )
  set_tests_properties(architecture_violation_rejected PROPERTIES WILL_FAIL TRUE)
endif()

fw_enforce_architecture()
