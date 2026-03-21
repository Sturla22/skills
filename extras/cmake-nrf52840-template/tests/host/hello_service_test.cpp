#include "starter/contracts/console.hpp"
#include "starter/domain/hello_service.hpp"

#include <iostream>
#include <string>

namespace
{
class FakeConsole final : public starter::contracts::Console
{
public:
    void write_line(const char* message) override
    {
        last_line = message;
    }

    std::string last_line;
};
} // namespace

int main()
{
    FakeConsole console;
    starter::domain::HelloService hello_service;

    hello_service.greet(console);

    if (console.last_line != "Hello, nRF52840!")
    {
        std::cerr << "unexpected greeting: " << console.last_line << '\n';
        return 1;
    }

    return 0;
}
