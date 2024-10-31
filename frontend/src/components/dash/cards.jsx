import React, { useState } from 'react';
import { CiHeart } from "react-icons/ci";
import { FaEdit } from "react-icons/fa";
import { MdDelete } from "react-icons/md";
import { FaPlus } from "react-icons/fa6";

function Cards({ home, SetInputDiv }) {
    const [tasks, setTasks] = useState([]);
    const [isSaved, setIsSaved] = useState(false);

    const handleSaveTask = (newTask) => {
        setTasks([...tasks, newTask]);
        setIsSaved(true);
    };

    return (
        <div className="grid grid-cols-3 gap-4 p-4">
            {tasks.length > 0 && tasks.map((task, i) => (
                <div key={i} className='bg-gray-800 rounded-sm p-4 flex flex-col justify-between'>
                    <div>
                        <h3 className='text-xl font-semibold'>{task.title}</h3>
                        <p className='text-gray-300 my-2'>{task.desc}</p>
                    </div>
                    <div className='mt-4 w-full flex items-center'>
                        <button className={`${task.status === "Incomplete" ? "bg-orange-700" : "bg-green-700"} p-2 rounded w-3/6`}>
                            {task.status}
                        </button>
                        {isSaved && (
                            <div className='text-white p-2 w-3/6 text-2xl font-semibold flex justify-around'>
                                <button><CiHeart /></button>
                                <button><FaEdit /></button>
                                <button><MdDelete /></button>
                            </div>
                        )}
                    </div>
                </div>
            ))}
            {home === "true" && (
                <button 
                    className='bg-gray-800 rounded-sm p-4 flex flex-col justify-center items-center text-gray-200 hover:scale-105 hover:cursor-pointer transition-all duration-300' 
                    onClick={() => SetInputDiv("fixed")}
                >
                    <FaPlus className='text-4xl'/>
                    <h2 className='text-2xl mt-4'>Add Task</h2>
                </button>
            )}
        </div>
    );
}

export default Cards;
