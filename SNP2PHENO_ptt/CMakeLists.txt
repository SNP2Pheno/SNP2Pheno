cmake_minimum_required(VERSION 3.30)
project(SNP2PHENO_ptt)

set(CMAKE_PREFIX_PATH "$ENV{HOME}/Qt6.9.0/lib/cmake")
set(CMAKE_CXX_STANDARD 23)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets Quick Qml QuickControls2)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)


add_executable(SNP2PHENO_ptt
        main.cpp
        debugconsole.cpp
        vcfparsercontroller.cpp
        vcf_to_snp.cpp
        vcfworker.h
        vcf_to_snp.h
        vcfparsercontroller.h
        debugconsole.h
        vcfworker.cpp
)

target_link_libraries(SNP2PHENO_ptt
        PRIVATE
        Qt6::Core
        Qt6::Gui
        Qt6::Widgets
        Qt6::Quick
        Qt6::Qml
        Qt6::QuickControls2 # optional but useful if you're using QML UI controls
)
