import axios from 'axios'
import { useState } from 'react'
const BASE_URL = "http://localhost:8000/"
const LOGIN_URL = "http://localhost:8000/api/token/"
const REFRESH_URL = "${LOGIN_URL}refresh/" 

export const login = async (username , password)=> {

    const response = await axios.post(LOGIN_URL,
        {username:username , password:password},
        {withCredentials:true}
    )
    return(
        response.data.success
    )

}

export const refresh_token = async()=> {
    await axios.post(REFRESH_URL,
        {},
        {withCredentials:true}
    )
    return true
}

const call_refresh = async(error,func) => {
    if(error.response && error.response.status === 401){
        const tokenRefreshed = await refresh_token();
        if (tokenRefreshed){
            const retryResponse = await func();
            return retryResponse.data
        }
    }
    return false
}

export const post_vote = async(rating)=>{
    try {
        const response = await axios.post(
            "http://localhost:8000/movies/:movieID",
            {"rating":rating},
            {withCredentials:true}
        )
        return response.data
    }catch(error){
        return call_refresh(error,
            axios.post("http://localhost:8000/movies/:movieID",{"rating":rating},{withCredentials:true}
        ))
    }
}