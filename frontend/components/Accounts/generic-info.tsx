import { Columns } from 'react-bulma-components'
import { User } from '../../types'

interface GenericInfoProps {
  user: User
}

const GenericInfo = ({ user }: GenericInfoProps) => {
  return (
    <Columns>
      <Columns.Column>
        {user.first_name} {user.last_name}
      </Columns.Column>
      <Columns.Column>{user.pennid}</Columns.Column>
    </Columns>
  )
}

export default GenericInfo
