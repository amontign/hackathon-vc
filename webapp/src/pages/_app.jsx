import '@/styles/globals.css'
import Head from 'next/head'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import { Outfit } from 'next/font/google'
import { Toaster } from 'react-hot-toast'

const outfit = Outfit({ subsets: ['latin'] })

export default function App({ Component, pageProps }) {

	return (
		<>
            <Head>
                <title>Hackathon - VC</title>
                <meta name="description" content="" />
                <meta name="keywords" content="" />
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <Toaster />
            {/*<Header />*/}
            <main className={outfit.className + " min-h-[calc(100vh-13.5rem)]"}>
                <Component {...pageProps} />
            </main>
            {/*<Footer />*/}
		</>
	)
}   