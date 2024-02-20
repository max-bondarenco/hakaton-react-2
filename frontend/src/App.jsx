import React, { useState } from 'react'

const App = () => {
    const [data, setData] = useState({})

    fetch('http://localhost:8000/auction/react/', {
        method: 'GET',
        mode: 'no-cors',
    })
        .then((res) => res.json())
        .then((data) => setData(data))
        .catch((err) => console.log(err))

    console.log(data)

    return <div>asdasdas</div>
}

export default App
