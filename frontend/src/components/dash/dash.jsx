import React from 'react';
import Sidebar from './sidebar';
import { Outlet } from 'react-router-dom';
import CurrentDate from './CurrentDate';

function Dash() {

    return (
        <div className='flex bg-orange-800 text-gray-200 h-screen w-screen p-2 gap-4'>
            <div className='w-1/6 border-gray-500 rounded-xl p-4 flex flex-col justify-between'>
                <Sidebar/>
            </div>
            <div className='w-5/6 border rounded-xl p-4'>
                <CurrentDate/>
                <Outlet/>
            </div>
        </div>
    );
};

export default Dash;