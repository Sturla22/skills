#pragma once

#include "starter/contracts/console.hpp"

namespace starter::domain
{
class HelloService
{
public:
    void greet(contracts::Console& console) const;
};
}  // namespace starter::domain
