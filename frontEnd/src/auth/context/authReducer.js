import { types } from "../types/types";

export const authReducer = (state = {} , action) => {
    switch(action.type){
        case types.login:
            return {
                ...state,//if more modifications with more properties
                logged: true,
                user: action.payload
            };
        case types.logout:
            return {
                logged: false
            };
        default:
            break
    }
}