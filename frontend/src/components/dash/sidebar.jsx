import React from 'react';
import { GrNotes } from "react-icons/gr";
import { MdLabelImportant } from "react-icons/md";
import { Link, useNavigate } from 'react-router-dom';



function Sidebar() {
    const data = [
        {
            title: "All tasks",
            icon: <GrNotes />,
            link: "alltasks",
        },
        {
            title: "Important tasks",
            icon: <MdLabelImportant />,
            link: "importantTasks",
        },
    ];

    const navigate = useNavigate();
    const handleLogout = () => {
        navigate('/');
    };

    return (
        <>
            <div>
                <h2 className='text-xl font-semibold'>Task-Master</h2>
                <h4 className='mb-1 text-gray-400'>Welcome back !!</h4>
                <hr/>
            </div>
            <div>
                {data.map((items, i) => (
                    <Link 
                        to={items.link} 
                        key={i} 
                        className='my-2 flex items-center hover:underline p-2 rounded transition-all duration-300'>
                        {items.icon}
                        <span className='ml-2'>{items.title}</span>
                    </Link>
            ))}
            </div>
            <div>
                <button className='bg-gray-800 w-full p-2 rounded' onClick={handleLogout}>Log Out</button>
            </div>
        </>
    );
};

export default Sidebar;