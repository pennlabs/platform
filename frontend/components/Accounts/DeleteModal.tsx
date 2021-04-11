// import { mutateResourceFunction } from "@pennlabs/rest-hooks/dist/types";
// import React from "react";
// import { Modal, Button } from "react-bulma-components";
// import { deleteContact } from "../../data-fetching/accounts";
// import { ContactType, User } from "../../types";
// import { logException } from "../../utils/sentry";

// interface DeleteModalProps {
//     type: ContactType;
//     id: number;
//     contact: string;
//     show: boolean;
//     closeFunc: () => void;
//     mutate: mutateResourceFunction<User>;
// }

// const DeleteModal = (props: DeleteModalProps) => {
//     const { show, closeFunc, type, contact, id, mutate } = props;
//     const prettyType = type === ContactType.Email ? "email" : "phone number";
//     const deleteContactMethod = async () => {
//         try {
//             await deleteContact(type, id);
//             closeFunc();
//             mutate();
//             // TODO: toast
//         } catch (e) {
//             logException(e);
//             // TODO: toast
//         }
//     };
//     return (
//         <Modal show={show} onClose={closeFunc}>
//             <Modal.Card>
//                 <Modal.Card.Head onClose={closeFunc}>
//                     <Modal.Card.Title>Are you sure?</Modal.Card.Title>
//                 </Modal.Card.Head>
//                 <Modal.Card.Body>
//                     Please confirm that you want to delete your {prettyType}:{" "}
//                     {contact}
//                     <br />
//                     <Button color="danger" onClick={deleteContactMethod}>
//                         Delete
//                     </Button>
//                 </Modal.Card.Body>
//             </Modal.Card>
//         </Modal>
//     );
// };

// export default DeleteModal;
