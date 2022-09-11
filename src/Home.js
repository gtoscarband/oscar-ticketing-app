import {useState} from "react";

export default function Home() {

    const [message, setMessage] = useState({
        color: "text-blue",
        message: "Please fill out the information and click Buy Now"
    })

    const handleSubmit = async (event) => {
        event.preventDefault();
        const {name, venmo_id, email, num_tickets} = event.target;

        const data = {
            name: name.value,
            venmo_id: venmo_id.value,
            email: email.value,
            num_tickets: num_tickets.value
        };

        const JSON_data = JSON.stringify(data);
        const endpoint = "/api/endpoints/request_payment"

        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON_data,
        }

        const response = await fetch(endpoint, options);
        let statusCode = response.status;

        if (statusCode === 200) {
            setMessage({
                color: "text-green-500",
                message: "Please check Venmo app for further instructions"
            })
        } else if (statusCode === 400) {
            setMessage({
                color: "text-red-600",
                message: await response.text()
            })
        }
    }

    return (
        <>
            <div className="h-screen overflow-hidden flex items-center justify-center" style={{background: "white"}}>
                <div
                    className="bg-blue-900 absolute top-0 left-0 bg-gradient-to-b from-gray-900 via-gray-900 to-blue-800 bottom-0 leading-5 h-full w-full overflow-hidden">
                    <svg className="relative block " style={{width: "calc(100% + 10px)"}} data-name="Layer 1"
                         xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
                        <path
                            d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z"
                            fill="#fff"></path>
                    </svg>
                </div>
                <div
                    className="relative  mt-20 sm:mt-0 min-h-screen  sm:flex sm:flex-row  justify-center bg-transparent p-6 sm:p-24 sm:pb-0 rounded-3xl shadow-xl">
                    {/* LEFT */}
                    <div className="flex-col flex  self-center lg:p-14 sm:max-w-4xl xl:max-w-md  z-10">
                        <div className="self-start hidden lg:flex flex-col  text-gray-300">
                            <h1 className="my-3 font-semibold text-4xl">GT Oscar Band Concert</h1>
                            <p className="pr-3 text-sm opacity-75">Concert Info: <br/> Lorem ipsum is placeholder text
                                commonly used in the graphic, print,
                                and publishing industries for previewing layouts and visual mockups</p>
                        </div>
                    </div>
                    {/* RIGHT */}
                    <div className="flex justify-center self-center  z-10">
                        <form
                            className="p-12 bg-gradient-to-b from-gray-900 via-gray-900 to-blue-800 mx-auto rounded-3xl w-96 "
                            onSubmit={handleSubmit}>
                            <div className="mb-7">
                                <h3 className="font-semibold text-2xl text-gray-300">Purchase Tickets </h3>
                            </div>
                            <div className="space-y-6">
                                <div>
                                    <input id='name' name="name"
                                           className=" w-full text-sm text-gray-300 px-4 py-3 bg-gray-900 border  border-gray-700 rounded-lg focus:outline-none focus:border-blue-400"
                                           type="" placeholder="Full Name" required/>
                                </div>
                                <div>
                                    <input id='venmo_id' name="venmo_id"
                                           className=" w-full text-sm text-gray-300 px-4 py-3 bg-gray-900 border  border-gray-700 rounded-lg focus:outline-none focus:border-blue-400"
                                           type="" placeholder="Venmo ID" required/>
                                </div>
                                <div>
                                    <input id='email' name="email" type="email"
                                           className=" w-full text-sm text-gray-300 px-4 py-3 bg-gray-900 border  border-gray-700 rounded-lg focus:outline-none focus:border-blue-400"
                                           placeholder="Email" required/>
                                </div>
                                <div>
                                    <input id='num_tickets' name="num_tickets" type="number"
                                           className=" w-full text-sm text-gray-300 px-4 py-3 bg-gray-900 border  border-gray-700 rounded-lg focus:outline-none focus:border-blue-400"
                                           placeholder="Number of Tickets" required/>
                                </div>
                            </div>
                            <div className="mt-7">
                                <button type="submit"
                                        className="w-full flex justify-center bg-blue-800  hover:bg-blue-700 text-gray-100 p-3  rounded-lg tracking-wide font-semibold  cursor-pointer transition ease-in duration-500">
                                    Buy Now
                                </button>
                            </div>
                            {
                                <div className="mt-7">
                                    <div
                                        className={`flex items-center ${message.color} text-xs px-4 py-3 italic text-center`}
                                        role="alert">
                                        <svg className="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg"
                                             viewBox="0 0 20 20">
                                            <path
                                                d="M12.432 0c1.34 0 2.01.912 2.01 1.957 0 1.305-1.164 2.512-2.679 2.512-1.269 0-2.009-.75-1.974-1.99C9.789 1.436 10.67 0 12.432 0zM8.309 20c-1.058 0-1.833-.652-1.093-3.524l1.214-5.092c.211-.814.246-1.141 0-1.141-.317 0-1.689.562-2.502 1.117l-.528-.88c2.572-2.186 5.531-3.467 6.801-3.467 1.057 0 1.233 1.273.705 3.23l-1.391 5.352c-.246.945-.141 1.271.106 1.271.317 0 1.357-.392 2.379-1.207l.6.814C12.098 19.02 9.365 20 8.309 20z"/>
                                        </svg>
                                        <p>{message.message}</p>
                                    </div>
                                </div>
                            }
                        </form>
                    </div>
                </div>
            </div>
        </>
    )
}
