import { Routes, Route } from 'react-router-dom'
import { Navigation } from './components/Navigation'
import { Auctions } from './pages/Auctions/Auctions'
import { User } from './pages/User'
import { Footer } from './components/Footer'
import axios from 'axios'

const getAuctions = async () => {
    let auctions

    console.log('blyad')
    axios
        .get('http://localhost:3000/api/auctions')
        .then((response) => (auctions = response.data))
        .catch((err) => console.log('Idi naxui'))

    return auctions || []
}

const auctions = await getAuctions()

export const App = () => {
    return (
        <>
            <Navigation />
            <Routes>
                <Route path="/" element={<Auctions auctions={auctions} />} />
                <Route path="/user" element={<User />} />
            </Routes>
            <Footer />
        </>
    )
}
