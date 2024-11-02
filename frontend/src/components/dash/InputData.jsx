import React, { useState, useEffect } from 'react';
import { ImCross } from "react-icons/im";

function InputData({ InputDiv, SetInputDiv, onSave, task }) {
    const [title, setTitle] = useState('');
    const [desc, setDesc] = useState('');

    // Set initial values based on the task being edited
    useEffect(() => {
        if (task) {
            setTitle(task.title);
            setDesc(task.desc);
        } else {
            setTitle('');
            setDesc('');
        }
    }, [task]);

    const handleSave = () => {
        if (title.trim() && desc.trim()) { 
            onSave({ ...task, title, desc, status: task ? task.status : 'Incomplete' }); 
            setTitle(''); 
            setDesc('');  
            SetInputDiv("hidden"); 
        } else {
            alert("Please fill in both fields"); 
        }
    };

    return (
        <>
            <div className={`${InputDiv} fixed top-0 left-0 bg-gray-800 opacity-80 h-screen w-full z-50`}></div>
            <div className={`${InputDiv} fixed top-0 left-0 flex items-center justify-center h-screen w-full z-50`}>
                <div className='w-1/3 bg-gray-900 p-6 rounded-lg shadow-lg'>
                    <div className='flex justify-end'>
                        <button className='text-2xl text-gray-300 hover:text-red-500 transition' onClick={() => SetInputDiv("hidden")}>
                            <ImCross />
                        </button>
                    </div>
                    <h2 className='text-white text-lg font-semibold mb-4'>{task ? "Edit Task" : "Add New Task"}</h2>
                    <input 
                        type='text' 
                        placeholder='Title' 
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        className='px-4 py-2 rounded-md w-full bg-gray-700 text-gray-200 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500'
                    />
                    <textarea 
                        name='desc' 
                        cols="30" 
                        rows="5" 
                        placeholder='Description...' 
                        value={desc}
                        onChange={(e) => setDesc(e.target.value)}
                        className='px-4 py-2 rounded-md w-full bg-gray-700 text-gray-200 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500'
                    ></textarea>
                    <button 
                        className='w-full px-4 py-2 bg-blue-500 rounded-md text-white text-lg font-semibold hover:bg-blue-600 transition'
                        onClick={handleSave}
                    >
                        Save
                    </button>
                </div>
            </div>
        </>
    );
}

export default InputData;
