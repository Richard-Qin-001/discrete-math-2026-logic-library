cmake_minimum_required(VERSION 3.16)
project(logic_benchmark LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

find_package(OpenMP REQUIRED)

set(COMMON_COMPILE_OPTIONS
    -O3
    -Wno-ignored-attributes
)

function(add_benchmark_target target_name source_file)
    add_executable(${target_name} ${source_file})
    target_compile_options(${target_name} PRIVATE ${COMMON_COMPILE_OPTIONS})
    target_link_libraries(${target_name} PRIVATE OpenMP::OpenMP_CXX)

    if(target_name MATCHES "avx512")
        target_compile_options(${target_name} PRIVATE -mavx512f -mavx512bw)
    elseif(target_name MATCHES "avx2")
        target_compile_options(${target_name} PRIVATE -mavx2)
    endif()
endfunction()

add_benchmark_target(checker utility/checker.cpp)
add_benchmark_target(generator utility/generator.cc)

add_benchmark_target(legacy source/legacy.cpp)
add_benchmark_target(recursion source/recursion.cpp)
add_benchmark_target(simd_ord_fill source/simd_ord_fill.cpp)
add_benchmark_target(simd_ord_precalc source/simd_ord_precalc.cpp)
add_benchmark_target(simd_avx2_fill source/simd_avx2_fill.cpp)
add_benchmark_target(simd_avx2_precalc source/simd_avx2_precalc.cpp)
add_benchmark_target(simd_avx2_omp_parallel source/simd_avx2_omp_parallel.cpp)
add_benchmark_target(simd_avx512_precalc source/simd_avx512_precalc.cpp)
add_benchmark_target(simd_avx512_omp_parallel source/simd_avx512_omp_parallel.cpp)
