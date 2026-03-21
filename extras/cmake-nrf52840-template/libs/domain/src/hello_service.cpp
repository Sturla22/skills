#include "starter/domain/hello_service.hpp"

namespace starter::domain
{
void HelloService::greet(contracts::Console& console) const
{
    console.write_line("Hello, nRF52840!");
}
}  // namespace starter::domain
