import { Auction } from './Auction'

export const Auctions = (props) => {
    return (
        <div>
            <div>
                <h1>Auctions</h1>
            </div>
            <div>
                {props.auctions.map((auction) => (
                    <Auction data={auction} />
                ))}
            </div>
        </div>
    )
}
