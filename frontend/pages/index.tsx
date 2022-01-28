import { GetServerSidePropsContext } from 'next'
import { Toaster } from 'react-hot-toast'

import { User } from '../types'
import Accounts from '../components/accounts'
import { withAuth } from '../utils/auth'

interface AccountPageProps {
  user: User
}

const AccountPage = ({ user }: AccountPageProps) => (
  <>
    <Toaster position="bottom-center" />
    <Accounts user={user} />
  </>
)

async function getServerSidePropsInner(_context: GetServerSidePropsContext) {
  return { props: {} }
}

export const getServerSideProps = withAuth(getServerSidePropsInner)

export default AccountPage
