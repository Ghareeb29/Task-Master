import React, { useState, useEffect } from 'react';
import { FaEdit } from "react-icons/fa";
import { MdDelete } from "react-icons/md";
import { FaPlus } from "react-icons/fa6";
import InputData from './InputData';

function Cards({ home, SetInputDiv }) {
    const [tasks, setTasks] = useState([]); 
    const [inputDiv, setInputDiv] = useState("hidden"); 
    const [editIndex, setEditIndex] = useState(null); 

    // Load tasks from localStorage on component mount
    useEffect(() => {
        const storedTasks = JSON.parse(localStorage.getItem('tasks')) || [];
        setTasks(storedTasks);
    }, []);

    // Update localStorage whenever tasks change
    const updateLocalStorage = (updatedTasks) => {
        setTasks(updatedTasks);
        localStorage.setItem('tasks', JSON.stringify(updatedTasks));
    };

    const handleSaveTask = (task) => {
        if (editIndex !== null) {
            // Edit existing task
            const updatedTasks = tasks.map((t, index) => (index === editIndex ? task : t));
            updateLocalStorage(updatedTasks);
            setEditIndex(null);
        } else {
            // Add new task
            const updatedTasks = [...tasks, task];
            updateLocalStorage(updatedTasks);
        }
        setInputDiv("hidden");
    };

    const handleEditTask = (index) => {
        setEditIndex(index);
        setInputDiv("flex"); 
    };

    const handleDeleteTask = (index) => {
        const updatedTasks = tasks.filter((_, i) => i !== index);
        updateLocalStorage(updatedTasks);
    };

    const handleToggleStatus = (index) => {
        const updatedTasks = tasks.map((t, i) => {
            if (i === index) {
                return { ...t, status: t.status === "Incomplete" ? "Complete" : "Incomplete" };
            }
            return t;
        });
        updateLocalStorage(updatedTasks);
    };

    return (
        <div>
            <div className="grid grid-cols-3 gap-4 p-4">
                {tasks.map((item, index) => (
                    <div key={index} className='bg-gray-800 rounded-sm p-4 flex flex-col justify-between'>
                        <div>
                            <h3 className='text-xl font-semibold'>{item.title}</h3>
                            <p className='text-gray-300 my-2'>{item.desc}</p>
                        </div>
                        <div className='mt-4 w-full flex items-center'>
                            <button 
                                className={`${item.status === "Incomplete" ? "bg-orange-700" : "bg-green-700"} p-2 rounded w-3/6`}
                                onClick={() => handleToggleStatus(index)} 
                            >
                                {item.status}
                            </button>
                            <div className='text-white p-2 w-3/6 text-2xl font-semibold flex justify-around'>
                                <button onClick={() => handleEditTask(index)}><FaEdit /></button>
                                <button onClick={() => handleDeleteTask(index)}><MdDelete /></button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {home === "true" && (
                <button 
                    className='bg-gray-800 rounded-sm p-4 flex flex-col justify-center items-center text-gray-200 hover:scale-105 hover:cursor-pointer transition-all duration-300' 
                    onClick={() => {
                        setEditIndex(null); 
                        setInputDiv("flex"); 
                    }}
                >
                    <FaPlus className='text-4xl'/>
                    <h2 className='text-2xl mt-4'>Add Task</h2>
                </button>
            )}

            <InputData 
                InputDiv={inputDiv} 
                SetInputDiv={setInputDiv} 
                onSave={handleSaveTask} 
                task={editIndex !== null ? tasks[editIndex] : null} 
            />
        </div>
    );
}

export default Cards;
