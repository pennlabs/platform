import { Modal, Button } from 'react-bulma-components'
import { ContactType } from '../../../types'

interface DeleteModalProps {
  type: ContactType
  contact: string
  show: boolean
  onDelete: () => void
  closeFunc: () => void
}

const DeleteModal = (props: DeleteModalProps) => {
  const { show, closeFunc, type, contact, onDelete } = props
  const prettyType = type === ContactType.Email ? 'email' : 'phone number'
  return (
    <Modal show={show} onClose={closeFunc}>
      <Modal.Card>
        <Modal.Card.Header onClose={closeFunc}>
          <Modal.Card.Title>{`Remove ${prettyType}?`}</Modal.Card.Title>
        </Modal.Card.Header>
        <Modal.Card.Body>
          {`You will no longer be able to use ${contact} with your account.`}
        </Modal.Card.Body>
        <Modal.Card.Footer>
          <Button color="link" onClick={onDelete}>
            Remove
          </Button>
        </Modal.Card.Footer>
      </Modal.Card>
    </Modal>
  )
}

export default DeleteModal
