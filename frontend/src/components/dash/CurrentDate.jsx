import React, {useState, useEffect} from 'react';

function CurrentDate() {

    const [currentDate, setCurrentDate] = useState(new Date());

    useEffect(() => {
        const intervalId = setInterval(() => {
            setCurrentDate(new Date());
        }, 1000);
        return () => clearInterval(intervalId);
    });

    return (
        <>
            <h1 className='text-gray-300 text-xl font-semibold'>Let's check your tasks!</h1>
            <h3 className='text-gray-400'>Small steps lead to big success</h3>
            <h3 className='text-gray-400'>Start achieving your goals</h3>
            <p>{currentDate.toLocaleString()}</p>
        </>
    );
};

export default CurrentDate;