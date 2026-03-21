cmake_minimum_required(VERSION 3.25)

project(invalid_domain_dep LANGUAGES CXX)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../../../cmake")
include(architecture)

add_library(contracts INTERFACE)
fw_register_target(contracts contracts)

add_library(platform INTERFACE)
target_link_libraries(platform INTERFACE contracts)
fw_register_target(platform platform)

add_library(domain INTERFACE)
target_link_libraries(domain INTERFACE platform)
fw_register_target(domain domain)

fw_enforce_architecture()
