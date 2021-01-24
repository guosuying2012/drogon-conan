from conans import ConanFile, CMake, tools


class DrogonConan(ConanFile):
    name = "drogon"
    version = "1.3.0"
    license = "MIT"
    author = "an-tao"
    url = "https://github.com/an-tao/drogon"
    description = "Drogon: A C++14/17 based HTTP web application framework running on Linux/macOS/Unix/Windows "
    topics = ("linux", " http", "http-server", "asynchronous-programming", "non-blocking-io", "drogon", "http-framework")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake", "cmake_find_package", "cmake_paths"
    requires = ["trantor/1.3.0", "jsoncpp/1.9.4", "libuuid/1.0.3", "zlib/1.2.11", "openssl/1.1.1i", "c-ares/1.17.1", "brotli/1.0.9", "libpq/13.1", "mariadb-connector-c/3.1.11", "sqlite3/3.34.0"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.run("git clone https://github.com/an-tao/drogon.git")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("drogon/CMakeLists.txt", "project(drogon)",
                              '''project(drogon)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR} ${CMAKE_MODULE_PATH})''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="drogon")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/drogon %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="drogon")
        self.copy("*drogon.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["drogon"]

