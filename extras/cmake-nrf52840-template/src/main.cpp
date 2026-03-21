#include "starter/domain/hello_service.hpp"
#include "starter/platform/semihost_console.hpp"

extern "C" void initialise_monitor_handles(void);

int main()
{
#if defined(STARTER_ENABLE_SEMIHOSTING)
    initialise_monitor_handles();
#endif

    starter::platform::SemihostConsole console;
    starter::domain::HelloService hello_service;
    hello_service.greet(console);

    for (;;)
    {
    }
}
