
-- Memory Address Table
    -- 0024 - Fireball 1 Flag / Explosion Delay (00-01 / 80-86)
    -- 0025 - Fireball 2 Flag / Explosion Delay (00-01 / 80-86)

    -- 0030 - Point display 3 timeout
    -- 0031 - Point display 2 timeout
    -- 0032 - Point display 1 timeout

    -- 0057 - Player X Delta (Signed)

    -- 008D - Fireball 1 X Position (00-FF)
    -- 008E - Fireball 2 X Position (00-FF)

    -- 009F - Player Y Delta (Signed)

    -- 00A6 - Fireball 1 Status? (03, FD, FE)
    -- 00A7 - Fireball 2 Status? (03, FD, FE)

    -- 00CE - Player Y Position

    -- 00D5 - Fireball 1 Y Position (00-FF)
    -- 00D6 - Fireball 2 Y Position (00-FF)

    -- 0200-02FF - PPU Sprite Memory
    -- 0300-03FF - Sprite Values
    -- 03A0 - Unknown Value, Gets set to FF every time a map is loaded.

    -- 0500-05CF - Screen layout page 1
    -- 05D0-069F - Screen layout page 2

    -- 06A0 - Screen Memory Offset

    -- 06CE - Fireball Count (00-FF)

    -- 06D5 - Player Sprite Frame

    -- 06D7 - End of Level Fireworks (Firework position is determined by value)

    -- 06FC - Controller 1 Poll

    -- 0700 - Running Animation Speed (00-28)
    -- 0701 - Sliding Flag (00 - No, 01 - Yes)
    -- 0702 - Slide Length
    -- 0703 - Matches Running Animation Speed from 1C-28
    -- 0704 - Unused?
    -- 0705 - Cycles during walking animation
    -- 0706 - Minimum Jump Height (01)
    -- 0707 - Always 01?
    -- 0708 - Starting Jump Y Position (Affects max jump height)
    -- 0709 - Player Y Delta While Jumping
    -- 070A - Player Y Delta Change To
    -- 070B - Player Injured Flag
    -- 070C - Walking Frame Delay (04-07)
    -- 070D - Player Frame While Walking (00-02)
    -- 070E - ? When Not 00, Player can't move or jump 
    -- 070F - ? When not 0, score at flag is visible before touched.
    -- 0710 - How Mario enters the level (00-07)
    --     00 - Fall from ceiling - Water (2-2)
    --     01 - Fall from ceiling - Underground (1-2)
    --     02 - On ground (1-1) Also, pipes and vines
    --     03 - Middle of screen for castles (1-4)
    --     04 - Unused: Same as 01
    --     05 - Unused: Same as 01 (maybe 02?)
    --     06 - Unused: Same as 07
    --     07 - On ground, Mario walks right (Between 1-1 and 1-2)
    -- 0711 - Delay (Used by throwing fireballs)
    -- 0712 - Unused?
    -- 0713 - Used during flag contact
    -- 0714 - Ducking Flag (00 - Walking, 04 - Ducking)

    -- 0747 - Object pause (When above zero, nothing but Mario can move. Used upon dieing)
    -- 0748 - Display Coins
    -- 074A - Controller 1 Poll
    -- 074B - Controller 2 Poll

    -- 074E - Background Type (00 - Under Water, 01 - Above Ground, 02 - Underground, 03 - Castle)

    -- 0754 - Tall Mario Flag (00 - Tall, 01 - Short)
    -- 0756 - Powerup Flag (00 - Mario, 01 - Super Mario, 02 - Fire Mario)
    -- 0757 - Player Lives Screen Flag (00 - Playing, 01 - Player Lives Screen)
    -- 0758 - Vine Growth Flag? Set to 1, die, restart, vine grows!
    -- 0759 - Time Up Flag (00-01) Doesn't take effect until after death
    -- 075A - Current Player Lives
    -- 075C - Display Level
    -- 075E - Display Coins
    -- 075F - World
    -- 0760 - Level
    -- 0761 - Waiting Player Lives

    -- 0770 - Gameplay Mode (00 - Demo, 01 - Playing, 02 - End of Level)
    -- 0772 - Gameplay Status (00 - Run to next status, 01 - Loading, 02 - Loading done, 03 - Playing)
    -- 0773-0774 - Counters for Gameplay Status

    -- 0778 - Affects Horizontal Scrolling
    -- 0779 - Color Mode? (1E - Color, 1F - Black & White)

    -- 077F - Delay (Used by demo, invincibility, and player lives screen)

    -- 0781 - Delay (Used by walking and throwing fireballs)
    -- 0782 - Delay (Used by jumping)

    -- 0787 - Timer Delay (00-18)

    -- 079F - Star Invincibility Timeout (00 - Not Invincible, 00-07 - Slow Flash, 08-FF - Fast Flash) - You can even kill Bowser's fireballs!

    -- 07A0 - Player Lives Countdown (00-07) At zero it starts the demo.
    -- 07A2 - Demo Countdown (00-07) At zero it starts the demo.

    -- 07D8 - Display Score: 9xxxx0
    -- 07D9 - Display Score: x9xxx0
    -- 07DA - Display Score: xx9xx0
    -- 07DB - Display Score: xxx9x0
    -- 07DC - Display Score: xxxx90

    -- 07DE - P1 Score: 9xxxx0
    -- 07DF - P1 Score: x9xxx0
    -- 07E0 - P1 Score: xx9xx0
    -- 07E1 - P1 Score: xxx9x0
    -- 07E2 - P1 Score: xxxx90
    -- 07E4 - P2 Score: 9xxxx0
    -- 07E5 - P2 Score: x9xxx0
    -- 07E6 - P2 Score: xx9xx0
    -- 07E7 - P2 Score: xxx9x0
    -- 07E8 - P2 Score: xxxx90

    -- 07ED - P1 Coins: 9x
    -- 07EE - P1 Coins: x9
    -- 07F3 - P2 Coins: 9x
    -- 07F4 - P2 Coins: x9

    -- 07F8 - Time: 9xx
    -- 07F9 - Time: x9x
    -- 07FA - Time: xx9

    -- 07FC - Beat Game Flag (00 - 1st Run, 01 - 2nd Run)

    -- B424 - Standing Max Jump Height (20) Signed
    -- B425 - Sliding Max Jump Height (20) Signed
    -- B426 - Walking Max Jump Height (1E) Signed
    -- B427 - Staring to Run Max Jump Height (28) Signed
    -- B428 - Running Max Jump Height (28) Signed

    -- B42B - Standing Gravity (70) Signed
    -- B42C - Sliding Gravity (70) Signed
    -- B42D - Walking Gravity (60) Signed
    -- B42E - Starting to Run Gravity (90) Signed
    -- B42F - Running Gravity (90) Signed

    -- B432 - Standing Jump Y Delta (FC) Signed
    -- B433 - Sliding Jump Y Delta (FC) Signed
    -- B434 - Walking Jump Y Delta (FC) Signed
    -- B435 - Starting to Run Jump Y Delta (FB) Signed
    -- B436 - Running Jump Y Delta (FB) Signed

    -- B440 - Left Running Speed Max (D8) Signed
    -- B441 - Left Walking Speed Max (E8) Signed
    -- B443 - Right Running Speed Max (28) Signed
    -- B444 - Right Walking Speed Max (18) Signed

    -- B447 - Running Acceleration (E4) Unsigned

-- user-defined parameters
pipe_in_file = pipe_in_file or "" -- pipe file through whcih the controller sends messages
pipe_out_file = pipe_out_file or "" -- pipe file through which the controller receives messages
target = target or "111"
verbose = verbose or false --- send back received message
frame_gap = frame_gap or 3
draw_tiles = draw_tiles or false
speedmode = speedmode or "maximum"

-- predefined parameters
commands = {}
screen = {}
last_processed_frame = 0
is_processing = false
pipe_in = nil
pipe_out = nil
started = false

addr = {}
addr["gameplay_status"] = 0x0772
addr["gameplay_mode"] = 0x0770
addr["current_page"] = 0x6d
addr["world"] = 0x075f
addr["level"] = 0x075c
addr["area"] = 0x0760
addr["life"] = 0x075a
addr["score"] = 0x07de
addr["time"] = 0x07f8
addr["coins"] = 0x07ed
addr["current_page"] = 0x6d
addr["x_position"] = 0x86
addr["y_position"] = 0x03b8
addr["y_viewport"] = 0x00b5
addr["player_state"] = 0x000e     -- x06 dies, x0b dying
addr["player_status"] = 0x0756    -- 0 = small, 1 = big, 2+ = fiery

distances = {}
distances["111"] = 3266    -- 1-1
distances["123"] = 3266    -- 1-2
distances["134"] = 2514    -- 1-3
distances["145"] = 2430    -- 1-4    
distances["211"] = 3298    -- 2-1
distances["223"] = 3266    -- 2-2
distances["234"] = 3682    -- 2-3
distances["245"] = 2430    -- 2-4    
distances["311"] = 3298    -- 3-1
distances["322"] = 3442    -- 3-2    
distances["333"] = 2498    -- 3-3
distances["344"] = 2430    -- 3-4
distances["411"] = 3698    -- 4-1
distances["423"] = 3266    -- 4-2
distances["434"] = 2434    -- 4-3
distances["445"] = 2942    -- 4-4
distances["511"] = 3282    -- 5-1
distances["522"] = 3298    -- 5-2
distances["533"] = 2514    -- 5-3
distances["544"] = 2429    -- 5-4
distances["611"] = 3106    -- 6-1
distances["622"] = 3554    -- 6-2
distances["633"] = 2754    -- 6-3
distances["644"] = 2429    -- 6-4
distances["711"] = 2962    -- 7-1
distances["723"] = 3266    -- 7-2
distances["734"] = 3682    -- 7-3
distances["745"] = 3453    -- 7-4
distances["811"] = 6114    -- 8-1
distances["822"] = 3554    -- 8-2
distances["833"] = 3554    -- 8-3
distances["844"] = 4989    -- 8-4

target_world = tonumber(string.sub(target, 1, 1))
target_level = tonumber(string.sub(target, 2, 2))
target_area =  tonumber(string.sub(target, 3, 3))


function readbyterange(address, length)
    local return_value = 0
    for offset = 0,length-1 do
      return_value = return_value * 10
      return_value = return_value + memory.readbyte(address + offset)
    end
    return return_value
end
function split(self, delimiter)
    local results = {}
    local start = 1
    local split_start, split_end  = string.find(self, delimiter, start)
    while split_start do
        table.insert(results, string.sub(self, start, split_start - 1))
        start = split_end + 1
        split_start, split_end = string.find(self, delimiter, start)
    end
    table.insert(results, string.sub(self, start))
    return results
end

function get_gameplay_status()
    return memory.readbyteunsigned(addr["gameplay_status"])
end
function get_gameplay_mode()
    return memory.readbyteunsigned(addr["gameplay_mode"])
end
function get_level()
    return memory.readbyte(addr["world"]) * 4 + memory.readbyte(addr["level"])
end
function get_x_position()
    return memory.readbyte(addr["x_position"])
end
function get_y_position()
    return memory.readbyte(addr["y_position"])
end
function get_distance()
    return memory.readbyte(addr["current_page"]) * 0x100 + get_x_position()
end
function get_score()
    return tonumber(readbyterange(addr["score"], 6))
end
function get_time()
    return tonumber(readbyterange(addr["time"], 3))
end
function get_coins()
    return tonumber(readbyterange(addr["coins"], 2))
end
function get_world_number()
    return memory.readbyte(addr["world"]) + 1
end
function get_level_number()
    return memory.readbyte(addr["level"]) + 1
end
function get_area_number()
    return memory.readbyte(addr["area"]) + 1
end
-- get_y_viewport - Returns the current y viewport
-- 1 = in visible viewport, 0 = above viewport, > 1 below viewport (i.e. dead)
function get_y_viewport()
    return memory.readbyte(addr["y_viewport"])
end
-- get_is_dead - Returns 1 if the player is dead or dying
-- 0x06 means dead, 0x0b means dying
function get_is_dead()
    local player_state = memory.readbyte(addr["player_state"])
    if (player_state == 0x06) or (player_state == 0x0b) or (get_y_viewport() > 1) then
        return 1
    else
        return 0
    end
end
function get_life()
    if (get_is_dead() == 1) then
        return 0
    end
    return memory.readbyte(addr["life"]) + 1
end
-- get_player_status - Returns the player status
-- 0 is small, 1 is big, 2+ is fiery (can shoot fireballs)
function get_player_status()
    return memory.readbyte(addr["player_status"])
end

function create_pipes()
    pipe_out = io.open(pipe_in_file, "w")
    pipe_in = io.open(pipe_out_file, "r")
end

function close_pipes()
    if pipe_in then
        pipe_in:close()
    end
    if pipe_out then
        pipe_out:close()
    end
end

function notify(message)
    if message and pipe_out then
        --local msg = message
        --if string.match(message, ".-#") ~= nil then
        --    msg = string.match(message, ".-#")
        --end
        -- print("send " .. msg)
        pipe_out:write(message .. "!\n")
        pipe_out:flush()
    end
end

function send_state(frame_number)
    --print("function send_state(frame_number)")
    local msg = "info_" .. frame_number .. "#"
    msg = msg .. "distance:" .. get_distance()
    msg = msg .. "|life:" .. get_life()
    msg = msg .. "|score:" .. get_score()
    msg = msg .. "|coins:" .. get_coins()
    msg = msg .. "|time:" .. get_time()
    msg = msg .. "|player_status:" .. get_player_status()
    msg = msg .. "|is_dead:" .. get_is_dead()
    if game_over() then
        msg = msg .. "|over:" .. 1
    else
        msg = msg .. "|over:" .. 0
    end
    notify(msg) 
    --print("ocal r, g, b, p")
    local r, g, b, p
    -- NES only has y values in the range 8 to 231, so we need to offset y values by 8
    local offset_y = 8
    
    for y=0,223 do
        --print("y1=" .. y)
        local screen_string = ""
        local data_count = 0        
        for x=0,255 do
            r, g, b, p = emu.getscreenpixel(x, y + offset_y, false)
            if p ~= screen[x][y] then
                screen[x][y] = p
                screen_string = screen_string .. "|" .. string.format("%02x%02x%02x", x, y, p)
                data_count = data_count + 1
            end
        end
        --print("y2=" .. y)
        if data_count > 0 then
            notify("screen_" .. frame_number .. "#" .. string.sub(screen_string, 2, -1))
        end
        --print("y3=" .. y)
    end
    --print("send_state end2")
    notify("done_" .. frame_number)
    --print("send_state end")
end

-- function render_tiles()
--     gui.box(
--         50 - 5 * 7 - 2,
--         70 - 5 * 7 - 2,
--         50 + 5 * 8 + 3,
--         70 + 5 * 5 + 3,
--         0,
--         "P30"
--     )      -- P30 = White (NES Palette 30 color)

--     -- Calculating tile types
--     for box_y = -4*16,8*16,16 do
--         local tile_string = "";
--         local data_count = 0;
--         for box_x = -7*16,8*16,16 do
--             -- 0 = Empty space
--             local tile_value = 0
--             local color = 0
--             local fill = 0
      
--             -- +1 = Not-Empty space (e.g. hard surface, object)
--             local curr_tile_type = get_tile_type(box_x, box_y)
--             if (curr_tile_type == 1) and (curr_y_position + box_y < 0x1B0) then
--                 tile_value = 1
--                 color = "P30" -- White (NES Palette 30 color)
--             end
      
--             -- +2 = Enemies
--             for i = 1,#enemies do
--                 local dist_x = math.abs(enemies[i]["x"] - (curr_x_position + box_x - left_x + 108))
--                 local dist_y = math.abs(enemies[i]["y"] - (90 + box_y))
--                 if (dist_x <= 8) and (dist_y <= 8) then
--                     tile_value = 2
--                     color = "P27" -- Orange (NES Palette 27 color)
--                     fill = "P3F" -- Black (NES Palette 3F color);
--                 end;
--             end;
            
--             -- +3 = Mario
--             local dist_x = math.abs(curr_x_position - (curr_x_position + box_x - left_x + 108));
--             local dist_y = math.abs(curr_y_position - (80 + box_y));
--             if (y_viewport == 1) and (dist_x <= 8) and (dist_y <= 8) then
--                 tile_value = 3;
--                 color = "P05"; -- Red (NES Palette 05 color)
--                 fill = color;
--             end;
            
--             -- Drawing tile
--             local tile_x = 50 + 5 * (box_x / 16);
--             local tile_y = 55 + 5 * (box_y / 16);
            
--             if (tile_value ~= 0) then
--                 gui.box(tile_x - 2, tile_y - 2, tile_x + 2, tile_y + 2, fill, color);
--             end
--         end
--     end
-- end

function fetch_command()
    --print("fetch_command ...")
    if pipe_in then
        --print("fetching ...")
        local line = pipe_in:read()
        --print("received:" .. line)
        if line then
            if verbose then
                notify("received: " .. line)
            end            

            local parts = split(line, "#")
            local header = parts[1] or ""
            local data = parts[2] or ""
            parts = split(header, "_")
            local command = parts[1] or ""
            local frame_number = parts[2] or ""

            if "commands" == command then
                commands_rcvd = 1
                parts = split(data, ",")
                commands["up"] = ((parts[1] == "1") or (parts[1] == "true"))
                commands["left"] = ((parts[2] == "1") or (parts[2] == "true"))
                commands["down"] = ((parts[3] == "1") or (parts[3] == "true"))
                commands["right"] = ((parts[4] == "1") or (parts[4] == "true"))
                commands["A"] = ((parts[5] == "1") or (parts[5] == "true"))
                commands["B"] = ((parts[6] == "1") or (parts[6] == "true"))
                commands["start"] = false
                commands["select"] = false

            elseif ("changelevel" == command) and (tonumber(data) >= 0) and (tonumber(data) <= 31) then
                local level = tonumber(data)
                target_world = math.floor(level / 4) + 1
                target_level = (level % 4) + 1
                target_area = target_level
                if (target_world == 1) or (target_world == 2) or (target_world == 4) or (target_world == 7) then
                    if (target_level >= 2) then
                        target_area = target_area + 1
                    end
                end
                target = target_world .. target_level .. target_area
                reset()
                emu.softreset()
        
            -- Exiting
            elseif "exit" == command then
                close_pipes()
                os.exit()
            end

        else
            return false
        end
    end
    return true
end

-- check_if_finished - Checks if the level is finished (life lost, finish line crossed, level increased)
-- The target (reward_threshold) is 40 pixels before the castle
-- The finish line (where the game will automatically close) is 15 pixels before the castle
function game_over()
    local distance = get_distance()

    if (get_life() < 3)
        or ((distance >= distances[target] - 15) and (distance <= distances[target]))
        or (get_level() > 4 * (target_world - 1) + (target_level - 1)) then
        return true
    end
    return false
end

function reset_commands()
    commands["up"] = false
    commands["down"] = false
    commands["left"] = false
    commands["right"] = false
    commands["A"] = false
    commands["B"] = false
    commands["start"] = false
    commands["select"] = false
end

function reset()
    reset_commands()
    for x=0,255 do
        screen[x] = {}
        for y=0,223 do
            screen[x][y] = -1
        end
    end
    started = false
    notify("reset")
end

function set_world_callback()
    if (get_world_number() ~= target_world) then
        memory.writebyte(addr["world"], (target_world - 1))
        memory.writebyte(addr["level"], (target_level - 1))
        memory.writebyte(addr["area"], (target_area - 1))
    end
end
function set_level_callback()
    if (get_level_number() ~= target_level) then
        memory.writebyte(addr["world"], (target_world - 1))
        memory.writebyte(addr["level"], (target_level - 1))
        memory.writebyte(addr["area"], (target_area - 1))
    end
end
function set_area_callback()
    if (get_area_number() ~= target_area) then
        memory.writebyte(addr["world"], (target_world - 1))
        memory.writebyte(addr["level"], (target_level - 1))
        memory.writebyte(addr["area"], (target_area - 1))
    end
end
function exit_callback()
    notify("exit")
    close_pipes()
end
memory.registerwrite(addr["world"], set_world_callback)
memory.registerwrite(addr["level"], set_level_callback)
memory.registerwrite(addr["area"], set_area_callback)
emu.registerexit(exit_callback)

emu.speedmode(speedmode)
reset()
create_pipes()
-- print("after create_pipes!")

function myerrorhandler( err )
    print( "ERROR:", err )
    print(debug.traceback())
end

function dump(o)
    if type(o) == 'table' then
        local s = '{ '
        for k,v in pairs(o) do
            if type(k) ~= 'number' then k = '"'..k..'"' end
            s = s .. '['..k..'] = ' .. dump(v) .. ','
        end
        return s .. '} '
    else
        return tostring(o)
    end
end

keep_commands = true
same_commands = 0
--print("while (true) do")
while (true) do
    if is_processing then
        -- print("return")
        return
    end
    is_processing = true

    local frame_count = emu.framecount()
    local is_playing = false

    if not keep_commands then
        reset_commands()
        keep_commands = true
        same_commands = 0
    end

    if get_gameplay_mode() == 0 then  -- at the start screen
        started = false
        is_playing = false
    elseif get_gameplay_status() == 3 then
        is_playing = true
    else
        is_playing = false            -- at the loading screen
    end
    
    if is_playing and not started then -- return game from the start screen
        started = true
        notify("ready_" .. frame_count-1)
        same_commands = 0
    end
    if not started and math.mod(frame_count, 100) == 0 then -- try to start game
        --print("try to start game")
        commands["start"] = true
        keep_commands = false
        same_commands = 0
    elseif is_playing and frame_count > frame_gap then
        --print("is_playing and frame_count > frame_gap then")
        if math.mod(frame_count, frame_gap) == 0 then
            --print("math.mod(frame_count, frame_gap) == 0")
            local last_commands = commands
            send_state(frame_count)
            --print("after send_state")
            while not fetch_command() do
            end
            if last_commands ~= commands then
                same_commands = 0
            end
        end
    end

    -- if same_commands > 100 and commands["A"] == true then  -- solve the problem of no jump when holding A for too long time
    --     commands["A"] = false
    --     joypad.set(1, commands)
    --     emu.frameadvance()
    --     same_commands = 0
    --     commands["A"] = true
    -- end

    -- local y = get_y_position()

    joypad.set(1, commands)
    gui.text(1, 8, get_distance())
    emu.frameadvance()

    -- if commands["A"] == true and y == get_y_position() and y == 176 then
        -- emu.message(same_commands)
    -- else
        same_commands = same_commands + 1
    -- end
    -- emu.message(same_commands .. " " .. tostring(commands["A"]))


    is_processing = false
end;
