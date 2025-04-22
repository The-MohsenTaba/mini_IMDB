import axios from 'axios'
const BASE_URL = "http://localhost:8000/"
const LOGIN_URL = "http://localhost:8000/api/token/"

export const login = async (username , password)=> {

    const response = await axios.post(LOGIN_URL,
        {username:username , password:password},
        {withCredentials:true}
    )
    return(
        response.data.success
    )

}