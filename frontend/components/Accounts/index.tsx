import { useResource } from '@pennlabs/rest-hooks'
import * as _ from 'lodash'
import * as Yup from 'yup'

import { Heading, Tabs } from 'react-bulma-components'
import { useState } from 'react'
import { Flex, Nav, MainContainer, CenterContainer, Logo } from './ui'
import { User } from '../../types'
import GenericInfoForm from './forms/generic-info-form'
import ContactInfoForm from './forms/contact-info-form'

const currentYear = new Date().getFullYear()

const FormSchema = Yup.object({
  first_name: Yup.string().required('Required'),
  student: Yup.object({
    graduation_year: Yup.number()
      .positive()
      .integer()
      .nullable()
      .min(currentYear)
      .max(currentYear + 10),
  }),
})

const selectFields = (form: User) => {
  const payload = _.cloneDeep(form)
  if (payload.student && !payload.student?.graduation_year) {
    payload.student.graduation_year = null
  }
  return {
    first_name: payload.first_name,
    student: payload.student,
  }
}

type Tab = 'general' | 'contact'

const Accounts = ({ user: initialUser }: { user: User }) => {
  const { data: userPartial, mutate } = useResource<User>('/accounts/me/', {
    initialData: initialUser,
  })
  const user = userPartial!

  const [tab, setTab] = useState<Tab>('general')

  return (
    <MainContainer>
      <Nav>
        <CenterContainer>
          <Flex
            margin="1rem 0.4rem"
            childMargin="0.2rem"
            justifyContent="flex-start"
          >
            <Logo src="/beaker.png" />
            <h4>Platform</h4>
          </Flex>
        </CenterContainer>
      </Nav>
      <CenterContainer>
        <div>
          <Heading>{`Welcome, ${user.first_name}`}</Heading>
          <Tabs size="medium">
            <Tabs.Tab
              onClick={() => setTab('general')}
              active={tab === 'general'}
            >
              General
            </Tabs.Tab>
            <Tabs.Tab
              onClick={() => setTab('contact')}
              active={tab === 'contact'}
            >
              Contact Info
            </Tabs.Tab>
          </Tabs>
          {tab === 'general' && (
            <>
              <div className="has-text-grey mb-4">
                {user.pennid} - {user.first_name} {user.last_name}
              </div>
              <GenericInfoForm mutate={mutate} initialData={user} />
            </>
          )}
          {tab === 'contact' && <ContactInfoForm initialData={user} />}
        </div>
      </CenterContainer>
    </MainContainer>
  )
}
export default Accounts
