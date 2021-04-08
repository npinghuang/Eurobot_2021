
    void AngleTransform(float x, float y, float z, float w){
        pitch = atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y));
        pitch *= -1;
        pitch /= 3.1415926;
        pitch *= 180;
        if(pitch < 0)
            pitch += 360;
        roll = asin( 2 * (w * y - x * z));
        roll *= -1;
        roll /= 3.1415926;
        roll *= 180;
        if(roll < 0 )
            roll += 360;
        yaw = atan2(2 * (w * z + x * y), 1 - 2 * (y * y - z * z));
        yaw *= -1;
        yaw /= 3.1415926;
        yaw *= 180;
        if(yaw < 0)
            yaw += 360;
    }
