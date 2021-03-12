import styled from "styled-components";

export const Flex = styled.div<{ margin?: string, childMargin?: string }>`
  display: flex;
  align-items: center;
  justify-content: center;
  margin: ${(props) => props.margin};

  & > * {
    margin: ${(props) => props.childMargin};
  }
`;

export const Nav = styled.div`
  background: #FEFEFE;
  box-shadow: 0px 2px 10px rgba(185, 185, 185, 0.32);
  display: flex;
  align-items: center;
  position: absolute;
  width: 100%;
`;

export const MainContainer = styled.div`
  background: #F7FBFF;
  display: flex;
  height: 100%;
  justify-content: center;
  align-items: center;
`;

export const CenterContainer = styled.div`
  width: 40%;
  height: 85%;
`;

export const Logo = styled.img`
  width: 1.2rem;
  height: 1.2rem;
`

export const Break = styled.hr`
  border: 1px solid #D3D3D3;
`

export const Text = styled.span<{ weight: string }>`
  font-weight: ${(props) => props.weight};
  font-size: 1rem;
`

export const FormGroupHeader = styled.h3`
  font-style: normal;
  font-weight: 600;
`

export const FormGroupGrid = styled.div`
  display: grid;
  grid-template-columns: 4fr 8fr;
  grid-auto-rows: 3rem;
`

interface FormGroupItemProps {
  col: number;
  row: number;
}

export const FormGroupItem = styled.div<FormGroupItemProps>`
  grid-column: ${(props) => props.col};
  grid-row: ${(props) => props.row};
  display: flex;
  align-items: center;
`

export const FormInput = styled.input`
  height: 2.3rem;
  width: 100%;
  outline: none;
  border: solid 1px #d6d6d6;
  border-radius: 0.2rem 0.2rem 0.2rem 0.2rem;
  padding-left: 0.3rem;
`;

export const Indicator = styled.img`
  width: 1rem;
  padding-top: 0.1rem;
`;

export const Tag = styled.div`
  height: 1rem;
  margin-top: 0.35rem;
  background-color: #E7E7E7;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.1rem;

  & > * {
    margin: 0.2rem;
    font-size: 0.5rem;
    font-weight: 600;
    color: #767676;
  }
`;

export const AddButton = styled.button`
  background: none!important;
  padding: 0!important;
  border: none;
  cursor: pointer;
  color: #209CEE;
  font-size: 1rem;
  font-weight: 500;
`;



export const selectStyles = {
  container: (base) => ({
    ...base, width: "100%"
  })
};
