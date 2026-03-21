#include "starter/platform/semihost_console.hpp"

#include <cstdio>

namespace starter::platform
{
void SemihostConsole::write_line(const char* message)
{
    std::fputs(message, stdout);
    std::fputc('\n', stdout);
    std::fflush(stdout);
}
} // namespace starter::platform
