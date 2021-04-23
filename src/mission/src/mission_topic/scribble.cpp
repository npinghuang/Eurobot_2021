void ST2_tx_transform_innerhand_1( int hand1, int hand2, int suck, int platform){
    if ( hand2 == -1){
        ST2_tx[0] =  pow(2,hand_ST2(hand1));   
        // ROS_INFO("mission hand %d %d", hand1, hand_ST2(hand1));
    }
    else{
        ST2_tx[0] =  pow(2, hand_ST2(hand1)) +  pow(2, hand_ST2(hand2));
        // ROS_INFO("debug hand 1 [%d] hand 2 [%d] st 1 [%d] st2 [%d]", hand1, hand2,  hand_ST2(hand1), hand_ST2(hand2));
    }
    ST2_tx[1] = suck;
    ST2_tx[2] = 404;
    ST2_tx[3] = platform;
    ST2_tx[4] = platform;
    ST2_tx[5] = 2;
    print_tx();
    // ROS_INFO("innerhand: hand = [%d, %d], suck = [%d], hand ST2 [%d]", hand1, hand2, suck, ST2_tx[0]);
    // publish_ST2();
    // onesec.sleep();
}
void  ST2_tx_transform_outterhand_1( int hand, int suck, int degree, int platform, int up_down){
    int hand_st = hand_ST2(hand);
    ROS_INFO("mission hand %d %d", hand, hand_ST2(hand));
    if ( hand <= 12){
        ST2_tx[0] = pow(2, hand_st);
    }
    else{
        ST2_tx[0] = hand_st;
    }
    ST2_tx[1] = suck;
    ST2_tx[2] = degree;
    if ( hand_st % 2 == 0){ // hand is on right platform
        ST2_tx[3] = platform;
        ST2_tx[4] = 2;
    }
    else if ( hand_st % 2 == 1){ // hand is on left platform
        ST2_tx[4] = platform;
        ST2_tx[3] = 2;
    }
    ST2_tx[5] = up_down;    
    print_tx();
    ROS_INFO("outterhand: hand = [%d], suck = [%d], degree = [%d]", hand, suck, degree);
}