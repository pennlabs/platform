import styled from "styled-components";

export const Flex = styled.div<{ margin: string }>`
  display: flex;
  align-items: center;
  justify-content: center;
  margin: ${(props) => props.margin};
`


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

export const Title = styled.h4`
  margin: 0.2rem;
`

export const Logo = styled.img`
  width: 1.2rem;
  height: 1.2rem;
  margin-left: 0.2rem;
  margin-right: 0.2rem;
`

export const Break = styled.hr`
  border: 1px solid #D3D3D3;
`

export const Text = styled.span<{ weight: string }>`
  font-weight: ${(props) => props.weight};
  font-size: 0.9rem;
`

export const FormGroupHeader = styled.h3`
  font-style: normal;
  font-weight: 600;
`

export const FormGroupGrid = styled.div`
  display: grid;
  grid-template-columns: 4fr 8fr;
  grid-auto-rows: 2rem;
`

interface FormGroupItemProps {
  col: number;
  row: number;
}

export const FormGroupItem = styled.div<FormGroupItemProps>`
  grid-column: ${(props) => props.col};
  grid-row: ${(props) => props.row};
`

export const FormInput = styled.input`
  height: 1.5rem;
  width: 90%;
  outline: none;
  border: solid 1px #d6d6d6;
  border-radius: 0.2rem 0.2rem 0.2rem 0.2rem;
  padding-left: 0.3rem;
`
