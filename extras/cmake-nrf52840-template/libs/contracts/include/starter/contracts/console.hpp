#pragma once

namespace starter::contracts
{
class Console
{
public:
    virtual ~Console() = default;
    virtual void write_line(const char* message) = 0;
};
} // namespace starter::contracts
