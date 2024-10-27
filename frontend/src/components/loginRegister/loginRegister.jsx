import React, { useState } from 'react';
import './loginRegister.css';
import { FaUser, FaLock, FaEnvelope } from "react-icons/fa";


const LoginRegister = () => {

    const [action, setAction] = useState('');

    const registerLink = () => {
        setAction(' active');
    };

    const loginLink = () => {
        setAction('');
    };


    return (
        <div className={`wrapper${action}`}>
            <div className='form-box login'>
                <form action=''>
                    <h1>login</h1>
                    <div className='input-box'>
                        <input type='text' placeholder='Username' required />
                        <FaUser className='icon' />
                    </div>
                    <div className='input-box'>
                        <input type='password' placeholder='password' required />
                        <FaLock className='icon' />
                    </div>

                    <div className='remember-forgot'>
                        <label><input type='checkbox' />Remember me</label>
                        <a href='#'>Forgot password</a>
                    </div>

                    <button type='submit'>Login</button>

                    <div className='register-link'>
                        <p>Don't have an account? <a href='#' onClick={registerLink}>signup</a></p>
                    </div>
                </form>
            </div>

            <div className='form-box register'>
                <form action=''>
                    <h1>Register</h1>
                    <div className='input-box'>
                        <input type='text' placeholder='Username' required />
                        <FaUser className='icon' />
                    </div>
                    <div className='input-box'>
                        <input type='email' placeholder='email' required />
                        <FaEnvelope className='icon' />
                    </div>
                    <div className='input-box'>
                        <input type='password' placeholder='password' required />
                        <FaLock className='icon' />
                    </div>

                    <div className='remember-forgot'>
                        <label><input type='checkbox' />agree all terms and conditions</label>
                    </div>

                    <button type='submit'>signup</button>

                    <div className='register-link'>
                        <p>have an account? <a href='#' onClick={loginLink}>login</a></p>
                    </div>
                </form>
            </div>

        </div>
    );
};

export default LoginRegister;