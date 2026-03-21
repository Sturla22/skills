#pragma once

#include "starter/contracts/console.hpp"

namespace starter::platform
{
class SemihostConsole final : public contracts::Console
{
public:
    void write_line(const char* message) override;
};
} // namespace starter::platform
