cmake_minimum_required(VERSION 3.30)
project(SNP2PHENO_ptt)

set(CMAKE_PREFIX_PATH "$ENV{HOME}/Qt/6.9.3/gcc_64/lib/cmake/")
set(CMAKE_CXX_STANDARD 23)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets Quick Qml QuickControls2 Sql QmlModels)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Ressourcen (QML-Dateien etc.)
qt6_add_resources(SNP2PHENO_ptt resources.qrc)


# Quellcode-Dateien
add_executable(SNP2PHENO_ptt
        main.cpp
        sources/vcfparsercontroller.cpp
        sources/vcf_to_snp.cpp
        sources/vcfworker.cpp
        sources/windowlauncher.cpp
        sources/snpdatabase.cpp
        headers/vcfparsercontroller.h
        headers/vcf_to_snp.h
        headers/vcfworker.h
        headers/windowlauncher.h
        headers/snpdatabase.h
)

# Link mit Qt-Modulen
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