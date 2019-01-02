
addr = {}
addr["current_page"] = 0x6d
addr["x_position"] = 0x86
function get_distance()
    return memory.readbyte(addr["current_page"]) * 0x100 + memory.readbyte(addr["x_position"])
end

emu.speedmode("normal")
while true do
    emu.message("dist " .. get_distance())
    emu.frameadvance()
end
