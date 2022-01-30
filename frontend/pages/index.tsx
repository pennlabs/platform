import { GetServerSidePropsContext } from "next";
import { Toaster } from "react-hot-toast";

import Head from "next/head";
import { User } from "../types";
import Accounts from "../components/accounts";
import { withAuth } from "../utils/auth";

interface AccountPageProps {
    user: User;
}

const AccountPage = ({ user }: AccountPageProps) => (
    <>
        <Head>
            <title>PennLabs Account Management</title>
            <link rel="icon" href="/favicon.ico" />
            <meta
                name="description"
                content="Manage your PennLabs account details."
            />
        </Head>
        <Toaster position="bottom-center" />
        <Accounts user={user} />
    </>
);

async function getServerSidePropsInner(_context: GetServerSidePropsContext) {
    return { props: {} };
}

export const getServerSideProps = withAuth(getServerSidePropsInner);

export default AccountPage;
