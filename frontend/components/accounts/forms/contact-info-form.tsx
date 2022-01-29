import { Columns, Heading } from 'react-bulma-components'
import { ContactType, User } from '../../../types'
import { Flex } from '../ui'
import ContactInput from './contact-input'

interface ContactInfoProps {
  initialData: User
}

const ContactInfoForm = (props: ContactInfoProps) => {
  const { initialData: user } = props
  return (
    <div>
      <Columns breakpoint="desktop">
        <Columns.Column>
          <Heading size={5} mb={3}>
            Emails
          </Heading>
          <Flex
            flexDirection="column"
            alignItems="start"
            childMargin="0.2rem"
            width="100%"
          >
            <ContactInput
              route="/accounts/me/email/"
              initialData={user.emails}
              addText="Add an email"
              contactType={ContactType.Email}
            />
          </Flex>
        </Columns.Column>
        <Columns.Column>
          <Heading size={5} mb={3}>
            Phone Numbers
          </Heading>
          <Flex
            flexDirection="column"
            alignItems="start"
            childMargin="0.2rem"
            width="100%"
          >
            <ContactInput
              route="/accounts/me/phonenumber/"
              initialData={user.phone_numbers}
              addText="Add a phone number"
              contactType={ContactType.PhoneNumber}
            />
          </Flex>
        </Columns.Column>
      </Columns>
    </div>
  )
}

export default ContactInfoForm
