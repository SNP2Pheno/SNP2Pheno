cmake_minimum_required(VERSION 3.30)
project(SNP2PHENO_ptt)

set(CMAKE_PREFIX_PATH "/opt/Qt/6.9.0/macos/lib/cmake")
set(CMAKE_CXX_STANDARD 23)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets Quick Qml QuickControls2 Sql QmlModels)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

add_executable(SNP2PHENO_ptt
        main.cpp
        controller/Controller.cpp
        controller/Controller.h
)

target_link_libraries(SNP2PHENO_ptt
        PRIVATE
        Qt6::Core
        Qt6::Gui
        Qt6::Widgets
        Qt6::Quick
        Qt6::Qml
        Qt6::QuickControls2
        Qt6::Sql
        Qt6::QmlModels
)
