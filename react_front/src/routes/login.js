import { VStack,FormControl,FormLabel,Input, Button } from '@chakra-ui/react';

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/useAuth';
const nav= useNavigate

const Login = () => {

    const [username,setUsername] = useState('')
    const [password,setPassword] = useState('')
    const {loginUser} = useAuth();

    const handleLogin = ()=> {

        loginUser(username,password)
    }

    return (
        <VStack>
            <FormControl>
                <FormLabel>Username</FormLabel>
                <Input onChange={(e) => setUsername(e.target.value)} value={username} type='text' placeholder='Your username here' />
            </FormControl>
            <FormControl>
                <FormLabel>Password</FormLabel>
                <Input  onChange={(e) => setPassword(e.target.value)} value={password} type='password' placeholder='Your password here' />
            </FormControl>
            <Button onClick={handleLogin}>Login</Button>
        </VStack>
    )
} 

export default Login