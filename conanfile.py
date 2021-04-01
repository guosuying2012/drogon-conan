from conans import ConanFile, CMake, tools


class DrogonConan(ConanFile):
    name = "drogon"
    version = "1.4.1"
    license = "MIT"
    author = "an-tao"
    url = "https://github.com/an-tao/drogon"
    description = "Drogon: A C++14/17 based HTTP web application framework running on Linux/macOS/Unix/Windows "
    topics = ("linux", " http", "http-server", "asynchronous-programming", "non-blocking-io", "drogon", "http-framework")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake", "cmake_find_package", "cmake_paths"
    requires = ["openssl/1.1.1i", "trantor/1.3.0", "jsoncpp/1.9.4", "zlib/1.2.11", "brotli/1.0.9", "libpq/13.1", "mariadb-connector-c/3.1.11", "sqlite3/3.34.0", "hiredis/1.0.0"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            pass

    def requirements(self):
        if self.settings.os != "Windows":
            self.requires("libuuid/1.0.3")
            pass

    def source(self):
        self.run("git clone https://gitee.com/an-tao/drogon.git")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("drogon/CMakeLists.txt", "project(drogon)",
                              '''project(drogon)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR} ${CMAKE_MODULE_PATH})''')
        
        tools.replace_in_file("drogon/CMakeLists.txt", "add_subdirectory(trantor)", '''# add_subdirectory(trantor)''')
        tools.replace_in_file("drogon/examples/CMakeLists.txt", "${PROJECT_SOURCE_DIR}/trantor/trantor/tests/server.pem", ''' ''')

        if self.settings.os != "Windows":
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PUBLIC trantor)", '''target_link_libraries(${PROJECT_NAME} PUBLIC trantor ${CONAN_LIBS})''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PRIVATE dl)", '''target_link_libraries(${PROJECT_NAME} PRIVATE dl  ${CONAN_LIBS})''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PRIVATE shlwapi)", '''target_link_libraries(${PROJECT_NAME} PRIVATE shlwapi ${CONAN_LIBS})''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PUBLIC Boost::boost)", '''target_link_libraries(${PROJECT_NAME} PUBLIC Boost::boost  ${CONAN_LIBS})''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PUBLIC Jsoncpp_lib)", '''target_link_libraries(${PROJECT_NAME} PUBLIC Jsoncpp_lib  ${CONAN_LIBS})''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PRIVATE UUID_lib)", '''target_link_libraries(${PROJECT_NAME} PRIVATE UUID_lib  ${CONAN_LIBS})''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PRIVATE Brotli_lib)", '''target_link_libraries(${PROJECT_NAME} PRIVATE Brotli_lib  ${CONAN_LIBS})''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PRIVATE pg_lib)", '''target_link_libraries(${PROJECT_NAME} PRIVATE pg_lib  ${CONAN_LIBS})''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PRIVATE MySQL_lib)", '''target_link_libraries(${PROJECT_NAME} PRIVATE MySQL_lib  ${CONAN_LIBS})''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PRIVATE SQLite3_lib)", '''target_link_libraries(${PROJECT_NAME} PRIVATE SQLite3_lib  ${CONAN_LIBS})''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PRIVATE ZLIB::ZLIB)", '''target_link_libraries(${PROJECT_NAME} PRIVATE ZLIB::ZLIB  ${CONAN_LIBS})''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PRIVATE OpenSSL::SSL OpenSSL::Crypto)", '''target_link_libraries(${PROJECT_NAME} PRIVATE OpenSSL::SSL OpenSSL::Crypto  ${CONAN_LIBS})''')
            tools.replace_in_file("drogon/examples/CMakeLists.txt", "link_libraries(${PROJECT_NAME})", '''link_libraries(${PROJECT_NAME} ${CONAN_LIBS})''')
        else:
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PUBLIC trantor)", '''target_link_libraries(${PROJECT_NAME} PUBLIC trantor ${CONAN_LIBS} Rpcrt4)''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PRIVATE dl)", '''target_link_libraries(${PROJECT_NAME} PRIVATE dl  ${CONAN_LIBS} Rpcrt4)''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PRIVATE shlwapi)", '''target_link_libraries(${PROJECT_NAME} PRIVATE shlwapi ${CONAN_LIBS} Rpcrt4)''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PUBLIC Boost::boost)", '''target_link_libraries(${PROJECT_NAME} PUBLIC Boost::boost  ${CONAN_LIBS} Rpcrt4)''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PUBLIC Jsoncpp_lib)", '''target_link_libraries(${PROJECT_NAME} PUBLIC Jsoncpp_lib  ${CONAN_LIBS} Rpcrt4)''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PRIVATE UUID_lib)", '''target_link_libraries(${PROJECT_NAME} PRIVATE UUID_lib  ${CONAN_LIBS} Rpcrt4)''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PRIVATE Brotli_lib)", '''target_link_libraries(${PROJECT_NAME} PRIVATE Brotli_lib  ${CONAN_LIBS} Rpcrt4)''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PRIVATE pg_lib)", '''target_link_libraries(${PROJECT_NAME} PRIVATE pg_lib  ${CONAN_LIBS} Rpcrt4)''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PRIVATE MySQL_lib)", '''target_link_libraries(${PROJECT_NAME} PRIVATE MySQL_lib  ${CONAN_LIBS} Rpcrt4)''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PRIVATE SQLite3_lib)", '''target_link_libraries(${PROJECT_NAME} PRIVATE SQLite3_lib  ${CONAN_LIBS} Rpcrt4)''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PRIVATE ZLIB::ZLIB)", '''target_link_libraries(${PROJECT_NAME} PRIVATE ZLIB::ZLIB  ${CONAN_LIBS} Rpcrt4)''')
            tools.replace_in_file("drogon/CMakeLists.txt", "target_link_libraries(${PROJECT_NAME} PRIVATE OpenSSL::SSL OpenSSL::Crypto)", '''target_link_libraries(${PROJECT_NAME} PRIVATE OpenSSL::SSL OpenSSL::Crypto  ${CONAN_LIBS} Rpcrt4)''')
            tools.replace_in_file("drogon/examples/CMakeLists.txt", "link_libraries(${PROJECT_NAME})", '''link_libraries(${PROJECT_NAME} ${CONAN_LIBS} Rpcrt4)''')
        pass


        if not self.options.shared:
        	tools.replace_in_file("drogon/cmake_modules/FindBrotli.cmake", "find_library(BROTLICOMMON_LIBRARY NAMES brotlicommon)", '''find_library(BROTLICOMMON_LIBRARY NAMES brotlicommon-static)''')
        	tools.replace_in_file("drogon/cmake_modules/FindBrotli.cmake", "find_library(BROTLIDEC_LIBRARY NAMES brotlidec)", '''find_library(BROTLIDEC_LIBRARY NAMES brotlidec-static)''')
        	tools.replace_in_file("drogon/cmake_modules/FindBrotli.cmake", "find_library(BROTLIENC_LIBRARY NAMES brotlienc)", '''find_library(BROTLIENC_LIBRARY NAMES brotlienc-static)''')
        pass

    def build(self):
        cmake = CMake(self)
        if self.options.shared:
            cmake.definitions["BUILD_DROGON_SHARED"] = "On"
            pass
        cmake.configure(source_folder="drogon")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/drogon %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include/drogon", src="drogon/lib/inc/drogon", keep_path=False)
        self.copy("*.h", dst="include/drogon/utils", src="drogon/lib/inc/drogon/utils", keep_path=False)
        self.copy("*.h", dst="include/drogon/plugins", src="drogon/lib/inc/drogon/plugins", keep_path=False)
        self.copy("*.h", dst="include/drogon/orm", src="drogon/orm_lib/inc", keep_path=False)
        self.copy("*.h", dst="include/drogon/nosql", src="drogon/nosql_lib/redis/inc/drogon/nosql/", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("drogon_ctl*", dst="bin", src="bin", keep_path=False)
        self.copy("dg_ctl*", dst="bin", src="bin", keep_path=False)
        self.copy("webapp*", dst="bin", src="bin", keep_path=False)
        self.copy("webapp_test*", dst="bin", src="bin", keep_path=False)
        self.copy("client*", dst="bin", src="bin", keep_path=False)
        self.copy("benchmark*", dst="bin", src="bin", keep_path=False)
        self.copy("pipelining_test*", dst="bin", src="bin", keep_path=False)
        self.copy("websocket_test*", dst="bin", src="bin", keep_path=False)
        self.copy("multiple_ws_test*", dst="bin", src="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["drogon"]

