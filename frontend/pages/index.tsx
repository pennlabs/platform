import React from "react";
import { GetServerSidePropsContext } from "next";
import { ToastProvider } from "react-toast-notifications";
import { User } from "../types";
import Accounts from "../components/Accounts";
import { withAuth } from "../utils/auth";

interface AccountPageProps {
    user: User;
}

const AccountPage = ({ user }: AccountPageProps) => (
    <ToastProvider placement="bottom-center" autoDismiss={true}>
        <Accounts user={user} />
    </ToastProvider>
);

async function getServerSidePropsInner(_context: GetServerSidePropsContext) {
    return { props: {} };
}

export const getServerSideProps = withAuth(getServerSidePropsInner);

export default AccountPage;
