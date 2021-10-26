// Thrust types
NEGATIVE_LARGE = -2;
NEGATIVE_SMALL = -1;
NONE = 0;
POSITIVE_SMALL = 1;
POSITIVE_LARGE = 2;

let IposX  = 0;
let IposY  = 0;
let IposZ  = 0;
let Iyaw   = 0;
let Ipitch = 0;
let Iroll  = 0;

function approach(current, target, scale)
{
    let thrust_list = [-2, -1, 0, 1, 2];

    for (var i = 0; i < thrust_list.length; i++)
    {
        if (current + thrust_list[i] == target)
            return thrust_list[i];
    }

    if (current < target)
        return scale;

    if (current > target)
        return (scale * -1);

    // shouldn't get here
    return 0;
}

function get_thrust(pos, Ipos, min, max, target)
{
    thrust = 0;

    scale = 2;
    if (Math.abs(pos) < 1)
        scale = 2;

    if (pos > 0)
    {
        // set thrust in a way to adjust Ipos to where it needs to be at this phase
        if (pos < min)
            thrust = approach(Ipos, 0, scale);
        else if (pos > max)
            thrust = approach(Ipos, (target * -1), scale);
    }

    if (pos < 0)
    {
        // set thrust in a way to adjust Ipos to where it needs to be at this phase
        if (pos > (min * -1))
            thrust = approach(Ipos, 0, scale);
        else if (pos < (max * -1))
            thrust = approach(Ipos, target, scale);
    }
    
    return thrust;
    // return 0, -1, 1, -2, or 2
}

//
// This function is called on each simulation step.
//
// Input: The current position, rotation and time
// Output: The control commands
//
function calculateControl(
    posX,        // - forward        + backward
    posY,        // - left            + right
    posZ,        // - down            + up
    yaw,        // - right            + left
    pitch,        // - down            + up
    roll,        // - CW                + CCW
    yawRate,    // speed with which the yaw is changing
    pitchRate,    // speed with which the pitch is changing
    rollRate,    // speed with which the roll is changing
    time)        // in simulation steps, starts from 0
{
    var moveX        = NONE;
    var moveY        = NONE;
    var moveZ        = NONE;
    var rotYaw       = NONE;
    var rotPitch     = NONE;
    var rotRoll      = NONE;
    
    IposX += moveX = get_thrust(posX, IposX, 1.5, 4.5, 75); // bounce on dock
    IposY += moveY = get_thrust(posY, IposY, 0.1, 0.2, 40); // too much pogo
    IposZ += moveZ = get_thrust(posZ, IposZ, 0.1, 0.2, 40); // too much pogo

    Iyaw   += rotYaw   = get_thrust(yaw,     Iyaw, 0.2, 0.3, 1);  // perfect
    Ipitch += rotPitch = get_thrust(pitch, Ipitch, 0.2, 0.3, 1);  // perfect
    Iroll  += rotRoll  = get_thrust(roll,   Iroll, 0.2, 0.3, 1);  // perfect
        
    // Return the control commands you want executed
    return [moveX, moveY, moveZ, rotYaw, rotPitch, rotRoll];
}
