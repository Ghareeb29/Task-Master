import { React} from 'react';
import { CiHeart } from "react-icons/ci";
import { FaEdit } from "react-icons/fa";
import { MdDelete } from "react-icons/md";
import { FaPlus } from "react-icons/fa6";


function Cards({ home, SetInputDiv }) {
    const data = [
        {
            title: "Work Out",
            desc: "Leg Day - You have to go on time",
            status: "Incomplete",
        },
        {
            title: "Meeting",
            desc: "Important meeting start at 1 pm",
            status: "Complete",
        },
        {
            title: "Study",
            desc: "you have to make course project",
            status: "Incomplete",
        },
        {
            title: "Meet friends",
            desc: "Time is on 8 pm - enjoy",
            status: "Incomplete",
        },
    ];

    return (
        <div className="grid grid-cols-3 gap-4 p-4">
            {data && data.map((items, i) => (
            <div className='bg-gray-800 rounded-sm p-4 flex flex-col justify-between'>
                <div>
                    <h3 className='Text-xl font-semibold'>{items.title}</h3>
                    <p className='text-gray-300 my-2'>{items.desc}</p>
                </div>
                    <div className='mt-4 w-full flex items-center'>
                        <button className={`${items.status === "Incomplete" ? "bg-orange-700" : "bg-green-700"} p-2 rounded w-3/6`}>{items.status}</button>
                        <div className='text-white p-2 w-3/6 text-2xl font-semibold flex justify-around'>
                            <button><CiHeart /></button>
                            <button><FaEdit /></button>
                            <button><MdDelete /></button>
                        </div>
                    </div>
                
            </div>
            ))}
            {home === "true" && (
                <button className='bg-gray-800 rounded-sm p-4 flex flex-col justify-center items-center text-gray-200 hover:scale-105 hover:cursor-pointer transition-all duration-300' onClick={ () => SetInputDiv("fixed")}>
                    <FaPlus className='text-4xl'/>
                    <h2 className='text-2xl mt-4'>Add Task</h2>
                </button>
            )}
            
        </div>
    );
};

export default Cards;