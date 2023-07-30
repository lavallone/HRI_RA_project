(define (problem school)
    (:domain school)
    (:objects robot bin1 bin2 bin3
              A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A14 A15 A16 A17 A18 A19 A20 A21 A22 A23 A24 A25 A26 A27 A28 A29 A30
              B1 B2 B3 B4 B5 B6 B7 B8 B9 B10 B11 B12 B13 B14 B15 B16 B17 B18 B19 B20 B21 B22 B23 B24 B25 B26 B27 B28 B29 B30 B31 B32 B33 B34 B35 B36
              C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20
              D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11 D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22 D23 D24 D25
              E1 E2 E3 E4 E5 E6 E7 E8 E9 E10 E11 E12 E13 E14 E15 E16 E17 E18 E19 E20 E21 E22 E23 E24 E25 E26 E27 E28 E29 E30 E31 E32 E33 E34 E35 E36 E37 E38 E39 E40
              F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 F11 F12 F13 F14 F15 F16 F17 F18 F19 F20 F21 F22 F23 F24
              G1 G2 G3 G4 G5 G6 G7 G8 G9 G10 G11 G12 G13 G14 G15 G16 G17 G18
              H1 H2 H3 H4 H5 H6 H7 H8 H9 H10 H11 H12 H13 H14 H15 H16 H17 H18 H19 H20 H21 H22 H23 H24
              I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 I14 I15 I16 I17 I18 I19 I20 I21 I22 I23 I24 I25 I26 I27 I28 I29 I30 I31 I32 I33 I34 I35 I36 I37 I38 I39 I40 I41 I42 I43 I44 I45 I46 I47 I48 I49 I50 
              I51 I52 I53 I54 I55 I56 I57 I58 I59 I60 I61 I62 I63 I64 I65 I66 I67 I68 I69 I70 I71 I72 I73 I74 I75 I76 I77 I78 I79 I80 I81 I82 I83 I84 I85 I86 I87 I88 I89 I90 I91 I92 I93 I94 I95 I96 I97 I98 I99 I100 
              I101 I102 I103 I104 I105 I106 I107 I108
    )
    (:init (is_agent robot) (agent_at robot I90)
           (is_bin bin1) (is_bin bin2) (is_bin bin3) (=(level bin1) 2) (=(level bin2) 2) (=(level bin3) 1) 
           (bin_at bin1 C9) (bin_at bin2 E39) (bin_at bin3 H12)

            ;room A
            (adj A1 A2) (adj A1 A7) (adj A2 A1) (adj A2 A3) (adj A2 A8) (adj A3 A2) (adj A3 A9) (adj A3 A4) (adj A4 A3) (adj A4 A10) (adj A4 A5) (adj A5 A4) (adj A5 A11) (adj A5 A6) (adj A6 A5) (adj A6 A12)
            (adj A7 A1) (adj A7 A8) (adj A7 A13) (adj A8 A2) (adj A8 A7) (adj A8 A9) (adj A8 A14) (adj A9 A3) (adj A9 A8) (adj A9 A10) (adj A9 A15) (adj A10 A4) (adj A10 A9) (adj A10 A11) (adj A10 A16) (adj A11 A10) (adj A11 A5) (adj A11 A12) (adj A11 A6) (adj A12 A11) (adj A12 A18)
            (adj A13 A7) (adj A13 A14) (adj A13 A19) (adj A14 A8) (adj A14 A13) (adj A14 A15) (adj A14 A20) (adj A15 A9)  (adj A15 A14) (adj A15 A16) (adj A15 A21) (adj A16 A15) (adj A16 A10) (adj A16 A17) (adj A16 A22) (adj A17 A16)  (adj A17 A18) (adj A17 A11) (adj A17 A23) (adj A18 A17) (adj A18 A12) (adj A18 A24)
            (adj A19 A20) (adj A19 A13) (adj A19 A25) (adj A20 A19) (adj A20 A21) (adj A20 A14) (adj A20 A26) (adj A21 A20) (adj A21 A22) (adj A21 A15) (adj A21 A27) (adj A22 A21) (adj A22 A23) (adj A22 A16) (adj A22 A28) (adj A23 A22) (adj A23 A24) (adj A23 A17) (adj A23 A29) (adj A24 A23) (adj A24 A18) (adj A24 A30)
            (adj A25 A26) (adj A25 A19) (adj A26 A27) (adj A26 A25) (adj A26 A20) (adj A27 A26) (adj A27 A28) (adj A27 A21) (adj A28 A27) (adj A28 A29) (adj A28 A22) (adj A29 A30) (adj A29 A28) (adj A29 A23) (adj A30 A29) (adj A30 A24)

            ;room B
            (adj B1 B2) (adj B1 B7) (adj B2 B1) (adj B2 B3) (adj B2 B8) (adj B3 B2) (adj B3 B9) (adj B3 B4) (adj B4 B3) (adj B4 B10) (adj B4 B5) (adj B5 B4) (adj B5 B11) (adj B5 B6) (adj B6 B5) (adj B6 B12)
            (adj B7 B1) (adj B7 B8) (adj B7 B13) (adj B8 B2) (adj B8 B7) (adj B8 B9) (adj B8 B14) (adj B9 B3) (adj B9 B8) (adj B9 B10) (adj B9 B15) (adj B10 B4) (adj B10 B9) (adj B10 B11) (adj B10 B16) (adj B11 B10) (adj B11 B5) (adj B11 B12) (adj B11 B6) (adj B12 B11) (adj B12 B18)
            (adj B13 B7) (adj B13 B14) (adj B13 B19) (adj B14 B8) (adj B14 B13) (adj B14 B15) (adj B14 B20) (adj B15 B9)  (adj B15 B14) (adj B15 B16) (adj B15 B21) (adj B16 B15) (adj B16 B10) (adj B16 B17) (adj B16 B22) (adj B17 B16) (adj B17 B18) (adj B17 B11) (adj B17 B23) (adj B18 B17) (adj B18 B12) (adj B18 B24)
            (adj B19 B20) (adj B19 B13) (adj B19 B25) (adj B20 B19) (adj B20 B21) (adj B20 B14) (adj B20 B26) (adj B21 B20) (adj B21 B22) (adj B21 B15) (adj B21 B27) (adj B22 B21) (adj B22 B23) (adj B22 B16) (adj B22 B28) (adj B23 B22) (adj B23 B24) (adj B23 B17) (adj B23 B29) (adj B24 B23) (adj B24 B18) (adj B24 B30)
            (adj B25 B26) (adj B25 B19) (adj B25 B31) (adj B26 B25)  (adj B26 B27) (adj B26 B20) (adj B26 B32) (adj B27 B26) (adj B27 B28) (adj B27 B21) (adj B27 B33) (adj B28 B27) (adj B28 B29)  (adj B28 B22) (adj B28 B34) (adj B29 B28) (adj B29 B35) (adj B29 B30) (adj B29 B23) (adj B30 B29) (adj B30 B24) (adj B30 B36)
            (adj B31 B25) (adj B31 B32) (adj B32 B31) (adj B32 B33) (adj B32 B27) (adj B33 B34) (adj B33 B32) (adj B33 B27) (adj B34 B33) (adj B34 B35) (adj B34 B28) (adj B35 B34) (adj B35 B36) (adj B35 B29) (adj B36 B35) (adj B36 B30)

            ;room C
            (adj C1 C2) (adj C1 C5) (adj C2 C1) (adj C2 C3) (adj C2 C6) (adj C3 C4)  (adj C3 C2) (adj C3 C7) (adj C4 C3) (adj C4 C8)
            (adj C5 C1)  (adj C5 C6) (adj C5 C9) (adj C6 C5) (adj C6 C7) (adj C6 C2) (adj C6 C10) (adj C7 C6) (adj C7 C8) (adj C7 C3) (adj C7 C11) (adj C8 C7) (adj C8 C4) (adj C8 C12)
            (adj C9 C5)  (adj C9 C10) (adj C9 C13) (adj C10 C9) (adj C10 C11) (adj C10 C6) (adj C10 C14) (adj C11 C10) (adj C11 C12) (adj C11 C7) (adj C11 C15) (adj C12 C11) (adj C12 C8) (adj C12 C16)
            (adj C13 C9) (adj C13 C14) (adj C13 C17) (adj C14 C13) (adj C14 C15) (adj C14 C10) (adj C14 C18) (adj C15 C14) (adj C15 C16) (adj C15 C11) (adj C15 C19) (adj C16 C15) (adj C16 C12) (adj C16 C20)
            (adj C17 C13) (adj C17 C18) (adj C18 C17) (adj C18 C19) (adj C18 C14) (adj C19 C18)  (adj C19 C20) (adj C19 C15) (adj C20 C16) (adj C20 C19)
          
            ;room D
            (adj D1 D2) (adj D1 D6) (adj D2 D1) (adj D2 D3) (adj D2 D7) (adj D3 D4)  (adj D3 D2) (adj D3 D8) (adj D4 D3) (adj D4 D5) (adj D4 D9) (adj D5 D4) (adj D5 D10)
            (adj D6 D1) (adj D6 D7) (adj D6 D11) (adj D7 D6) (adj D7 D8) (adj D7 D2) (adj D7 D12) (adj D8 D7) (adj D8 D9) (adj D8 D3) (adj D8 D13) (adj D9 D10) (adj D9 D8) (adj D9 D4) (adj D9 D14) (adj D10 D9) (adj D10 D5) (adj D10 D15)
            (adj D11 D12) (adj D11 D6) (adj D11 D16) (adj D12 D11) (adj D12 D13) (adj D12 D7) (adj D12 D17) (adj D13 D12) (adj D13 D14) (adj D13 D8) (adj D13 D18) (adj D14 D15) (adj D14 D13) (adj D14 D9) (adj D14 D19) (adj D15 D14) (adj D15 D20) (adj D15 D10)
            (adj D16 D17) (adj D16 D11) (adj D16 D21) (adj D17 D16) (adj D17 D18) (adj D17 D12) (adj D17 D22) (adj D18 D17) (adj D18 D19) (adj D18 D13) (adj D18 D23) (adj D19 D18) (adj D19 D20) (adj D19 D14) (adj D19 D24) (adj D20 D19) (adj D20 D15) (adj D20 D25)
            (adj D21 D22) (adj D21 D16) (adj D22 D21) (adj D22 D23) (adj D22 D17) (adj D23 D24)  (adj D23 D22) (adj D23 D18) (adj D24 D23) (adj D24 D25) (adj D24 D19) (adj D25 D24) (adj D25 D20)

            ;room E
            (adj E1 E2) (adj E1 E11) (adj E2 E1) (adj E2 E3) (adj E2 E12) (adj E3 E2) (adj E3 E4) (adj E3 E13) (adj E4 E3) (adj E4 E5) (adj E4 E14) (adj E5 E6) (adj E5 E4) (adj E5 E15) (adj E6 E5) (adj E6 E7) (adj E6 E16) (adj E7 E6) (adj E7 E8) (adj E7 E17) (adj E8 E7) (adj E8 E9) (adj E8 E17) (adj E9 E8) (adj E9 E10) (adj E9 E19) (adj E10 E9) (adj E10 E20)
            (adj E11 E12) (adj E11 E1) (adj E11 E21) (adj E12 E11) (adj E12 E13) (adj E12 E2) (adj E12 E22) (adj E13 E12) (adj E13 E14) (adj E13 E3) (adj E13 E23) (adj E14 E13) (adj E14 E15) (adj E14 E4) (adj E14 E24) (adj E15 E14) (adj E15 E16) (adj E15 E5) (adj E15 E25) (adj E16 E15) (adj E16 E17) (adj E16 E6) (adj E16 E26) (adj E17 E16) (adj E17 E18) (adj E17 E7) (adj E17 E27) (adj E18 E17) (adj E18 E19) (adj E18 E8) (adj E18 E28) (adj E19 E18) (adj E19 E20) (adj E19 E9) (adj E19 E29) (adj E20 E19) (adj E20 E10) (adj E20 E30)
            (adj E21 E22) (adj E21 E11) (adj E21 E31) (adj E22 E21) (adj E22 E23) (adj E22 E12) (adj E22 E32) (adj E23 E22) (adj E23 E24) (adj E23 E13) (adj E23 E33) (adj E24 E23) (adj E24 E25) (adj E24 E14) (adj E24 E34) (adj E25 E24) (adj E25 E26) (adj E25 E15) (adj E25 E35) (adj E26 E25) (adj E26 E27) (adj E26 E16) (adj E26 E36) (adj E27 E26) (adj E27 E28) (adj E27 E17) (adj E27 E37) (adj E28 E27) (adj E28 E29) (adj E28 E18) (adj E28 E38) (adj E29 E28) (adj E29 E30) (adj E29 E19) (adj E29 E39) (adj E30 E29) (adj E30 E20) (adj E30 E40)
            (adj E31 E32) (adj E31 E21) (adj E32 E31) (adj E32 E33) (adj E32 E22) (adj E33 E23) (adj E33 E32) (adj E33 E34) (adj E34 E33) (adj E34 E35) (adj E34 E24) (adj E35 E34) (adj E35 E36) (adj E35 E25) (adj E36 E35) (adj E36 E37) (adj E36 E26) (adj E37 E36) (adj E37 E38) (adj E37 E27) (adj E38 E37) (adj E38 E39) (adj E38 E28) (adj E39 E38) (adj E39 E40) (adj E39 E29) (adj E40 E39) (adj E40 E30)

            ;room F
            (adj F1 F2) (adj F1 F7) (adj F2 F1) (adj F2 F3) (adj F2 F8) (adj F3 F2) (adj F3 F9) (adj F3 F4) (adj F4 F3) (adj F4 F10) (adj F4 F5) (adj F5 F4) (adj F5 F11) (adj F5 F6) (adj F6 F5) (adj F6 F12)
            (adj F7 F1) (adj F7 F8) (adj F7 F13) (adj F8 F2) (adj F8 F7) (adj F8 F9) (adj F8 F14) (adj F9 F3) (adj F9 F8) (adj F9 F10) (adj F9 F15) (adj F10 F4) (adj F10 F9) (adj F10 F11) (adj F10 F16) (adj F11 F10) (adj F11 F5) (adj F11 F12) (adj F11 F6) (adj F12 F11) (adj F12 F18)
            (adj F13 F7) (adj F13 F14) (adj F13 F19) (adj F14 F8) (adj F14 F13) (adj F14 F15) (adj F14 F20) (adj F15 F9)  (adj F15 F14) (adj F15 F16) (adj F15 F21) (adj F16 F15) (adj F16 F10) (adj F16 F17) (adj F16 F22) (adj F17 F16)  (adj F17 F18) (adj F17 F11) (adj F17 F23) (adj F18 F17) (adj F18 F12) (adj F18 F24)
            (adj F19 F20) (adj F19 F13) (adj F20 F19) (adj F20 F21) (adj F20 F14) (adj F21 F20) (adj F21 F22) (adj F21 F15) (adj F22 F21) (adj F22 F16) (adj F22 F23) (adj F23 F22) (adj F23 F24) (adj F23 F17) (adj F24 F23) (adj F24 F18)

            ;room G
            (adj G1 G2) (adj G1 G7) (adj G2 G1) (adj G2 G3) (adj G2 G8) (adj G3 G2) (adj G3 G9) (adj G3 G4) (adj G4 G3) (adj G4 G10) (adj G4 G5) (adj G5 G4) (adj G5 G11) (adj G5 G6) (adj G6 G5) (adj G6 G12)
            (adj G7 G1) (adj G7 G8) (adj G7 G13) (adj G8 G2) (adj G8 G7) (adj G8 G9) (adj G8 G14) (adj G9 G3) (adj G9 G8) (adj G9 G10) (adj G9 G15) (adj G10 G4) (adj G10 G9) (adj G10 G11) (adj G10 G16) (adj G11 G10) (adj G11 G5) (adj G11 G12) (adj G11 G6) (adj G12 G11) (adj G12 G18)
            (adj G13 G7) (adj G13 G14) (adj G14 G8) (adj G14 G13) (adj G14 G15) (adj G15 G9) (adj G15 G14) (adj G15 G16) (adj G16 G15) (adj G16 G10) (adj G16 G17) (adj G17 G16) (adj G17 G18) (adj G17 G11) (adj G18 G17) (adj G18 G12)
            
            ;room H
            (adj H1 H2) (adj H1 H7) (adj H2 H1) (adj H2 H3) (adj H2 H8) (adj H3 H2) (adj H3 H9) (adj H3 H4) (adj H4 H3) (adj H4 H10) (adj H4 H5) (adj H5 H4) (adj H5 H11) (adj H5 H6) (adj H6 H5) (adj H6 H12)
            (adj H7 H1) (adj H7 H8) (adj H7 H13) (adj H8 H2) (adj H8 H7) (adj H8 H9) (adj H8 H14) (adj H9 H3) (adj H9 H8) (adj H9 H10) (adj H9 H15) (adj H10 H4) (adj H10 H9) (adj H10 H11) (adj H10 H16) (adj H11 H10) (adj H11 H5) (adj H11 H12) (adj H11 H6) (adj H12 H11) (adj H12 H18)
            (adj H13 H7) (adj H13 H14) (adj H13 H19) (adj H14 H8) (adj H14 H13) (adj H14 H15) (adj H14 H20) (adj H15 H9)  (adj H15 H14) (adj H15 H16) (adj H15 H21) (adj H16 H15) (adj H16 H10) (adj H16 H17) (adj H16 H22) (adj H17 H16) (adj H17 H18) (adj H17 H11) (adj H17 H23) (adj H18 H17) (adj H18 H12) (adj H18 H24)
            (adj H19 H20) (adj H19 H13) (adj H20 H19) (adj H20 H21) (adj H20 H14) (adj H21 H20) (adj H21 H22) (adj H21 H15) (adj H22 H21) (adj H22 H16) (adj H22 H23) (adj H23 H22) (adj H23 H24) (adj H23 H17) (adj H24 H23) (adj H24 H18)

            ;corridor + entrance = I
            (adj I1 I2) (adj I1 I5) (adj I2 I1) (adj I2 I6) (adj I3 I4) (adj I3 I7) (adj I4 I3) (adj I4 I8)
            (adj I5 I1) (adj I5 I6) (adj I5 I9) (adj I6 I2) (adj I6 I5) (adj I6 I10) (adj I7 I3) (adj I7 I8) (adj I7 I11) (adj I8 I7) (adj I8 I4) (adj I8 I12)
            (adj I9 I5) (adj I9 I10) (adj I9 I13) (adj I10 I6) (adj I10 I9) (adj I10 I14) (adj I11 I7) (adj I11 I12) (adj I11 I15) (adj I12 I8) (adj I12 I11) (adj I12 I16)
            (adj I13 I9) (adj I13 I14) (adj I13 I17) (adj I14 I10) (adj I14 I15) (adj I14 I18) (adj I15 I11) (adj I15 I16) (adj I15 I19) (adj I16 I12) (adj I16 I15) (adj I16 I20)
            (adj I17 I13) (adj I17 I18) (adj I17 I21) (adj I18 I14) (adj I18 I17) (adj I18 I22) (adj I19 I15) (adj I19 I20) (adj I19 I23) (adj I20 I16) (adj I20 I19) (adj I20 I24)
            (adj I21 I17) (adj I21 I22) (adj I21 I25) (adj I22 I18) (adj I22 I21) (adj I22 I26) (adj I23 I19) (adj I23 I24) (adj I23 I27) (adj I24 I20) (adj I24 I23) (adj I24 I28)
            (adj I25 I21) (adj I25 I26) (adj I25 I29) (adj I26 I22) (adj I26 I25) (adj I26 I30) (adj I27 I23) (adj I27 I28) (adj I27 I31) (adj I28 I24) (adj I28 I27) (adj I28 I32)
            (adj I29 I25) (adj I29 I30) (adj I29 I33) (adj I30 I26) (adj I30 I29) (adj I30 I34) (adj I31 I27) (adj I31 I32) (adj I31 I35) (adj I32 I28) (adj I32 I31) (adj I32 I36)
            (adj I33 I29) (adj I33 I34) (adj I33 I37) (adj I34 I30) (adj I34 I33) (adj I34 I38) (adj I35 I31) (adj I35 I36) (adj I35 I39) (adj I36 I32) (adj I36 I35) (adj I36 I40)
            (adj I37 I33) (adj I37 I38) (adj I37 I41) (adj I38 I34) (adj I38 I37) (adj I38 I42) (adj I39 I35) (adj I39 I40) (adj I39 I53) (adj I40 I36) (adj I40 I39) (adj I40 I54)
            ;
            (adj I41 I42) (adj I41 I37) (adj I41 I55) (adj I42 I38) (adj I42 I56) (adj I42 I41) (adj I42 I43) (adj I43 I42) (adj I43 I44) (adj I43 I57) (adj I44 I43) (adj I44 I45) (adj I44 I58) (adj I45 I44) (adj I45 I46) (adj I45 I59) (adj I46 I45) (adj I46 I47) (adj I46 I60) (adj I47 I46) (adj I47 I48) (adj I47 I61) (adj I48 I47) (adj I48 I49) (adj I48 I62) (adj I49 I50) (adj I49 I48) (adj I49 I63) (adj I50 I49) (adj I50 I51) (adj I50 I64) (adj I51 I50) (adj I51 I52) (adj I51 I65) (adj I52 I51) (adj I52 I53) (adj I52 I66) (adj I53 I52) (adj I53 I54) (adj I53 I39) (adj I53 I67) (adj I54 I53) (adj I54 I40) (adj I54 I68)
            (adj I55 I41) (adj I55 I56) (adj I56 I55) (adj I56 I57) (adj I56 I42) (adj I57 I56) (adj I57 I58) (adj I57 I43) (adj I58 I57) (adj I58 I59) (adj I58 I44) (adj I59 I58) (adj I59 I60) (adj I59 I43) (adj I59 I69) (adj I60 I61) (adj I60 I59) (adj I60 I46) (adj I60 I70) (adj I61 I60) (adj I61 I62) (adj I61 I47) (adj I61 I71) (adj I62 I61) (adj I62 I63) (adj I62 I48) (adj I62 I72) (adj I63 I62) (adj I63 I64) (adj I63 I49) (adj I63 I73) (adj I64 I63) (adj I64 I65) (adj I64 I50) (adj I64 I74) (adj I65 I64) (adj I65 I66) (adj I65 I51) (adj I65 I75) (adj I66 I65) (adj I66 I67) (adj I66 I52) (adj I66 I76) (adj I67 I66) (adj I67 I68) (adj I67 I53) (adj I67 I77) (adj I68 I67) (adj I68 I54) (adj I68 I78)
            (adj I69 I70) (adj I69 I59) (adj I69 I79) (adj I70 I69) (adj I70 I71) (adj I70 I60) (adj I70 I80) (adj I71 I72) (adj I71 I70) (adj I71 I61) (adj I71 I81) (adj I72 I71) (adj I72 I73) (adj I72 I62) (adj I72 I82) (adj I73 I72) (adj I73 I74) (adj I73 I63) (adj I73 I83) (adj I74 I73) (adj I74 I75) (adj I74 I64) (adj I74 I84) (adj I75 I74) (adj I75 I76) (adj I75 I65) (adj I76 I75) (adj I76 I77) (adj I76 I66) (adj I77 I76) (adj I77 I78) (adj I77 I67) (adj I78 I77) (adj I78 I68)
            ;
            (adj I79 I80) (adj I79 I69) (adj I79 I85) (adj I80 I79) (adj I80 I81)  (adj I80 I70)  (adj I80 I86) (adj I81 I80) (adj I81 I82) (adj I81 I71) (adj I81 I87) (adj I82 I81) (adj I82 I83) (adj I82 I72) (adj I82 I88) (adj I83 I82) (adj I83 I84) (adj I83 I73) (adj I83 I89) (adj I84 I83) (adj I84 I74) (adj I84 I90)
            (adj I85 I86) (adj I85 I79) (adj I85 I91) (adj I86 I85) (adj I86 I87)  (adj I86 I80)  (adj I86 I92) (adj I87 I86) (adj I87 I88) (adj I87 I81) (adj I87 I93) (adj I88 I87) (adj I88 I89) (adj I88 I82) (adj I88 I94) (adj I89 I88) (adj I89 I90) (adj I89 I83) (adj I89 I95) (adj I90 I89) (adj I90 I84) (adj I90 I96)
            (adj I91 I92) (adj I91 I85) (adj I91 I97) (adj I92 I91) (adj I92 I93)  (adj I92 I86)  (adj I92 I98) (adj I93 I92) (adj I93 I94) (adj I93 I87) (adj I93 I99) (adj I94 I93) (adj I94 I95) (adj I94 I88) (adj I94 I100) (adj I95 I94) (adj I95 I96) (adj I95 I89) (adj I95 I101) (adj I96 I95) (adj I96 I90) (adj I96 I102)
            (adj I97 I98) (adj I97 I91) (adj I97 I103) (adj I98 I97) (adj I98 I99)  (adj I98 I92)  (adj I98 I104) (adj I99 I98) (adj I99 I100) (adj I99 I93) (adj I99 I105) (adj I100 I99) (adj I100 I101) (adj I100 I94) (adj I100 I106) (adj I101 I100) (adj I101 I102) (adj I101 I95) (adj I101 I107) (adj I102 I101) (adj I102 I96) (adj I102 I108)
            (adj I103 I104) (adj I103 I97) (adj I104 I103) (adj I104 I105) (adj I104 I98) (adj I105 I104) (adj I105 I106) (adj I105 I99) (adj I106 I105) (adj I106 I107) (adj I106 I100) (adj I107 I106) (adj I107 I108) (adj I107 I101) (adj I108 I107) (adj I108 I102)

            ; all doors open
            (adj A12 I5) (adj I5 A12)
            (adj B18 I33) (adj I33 B18)
            (adj B33 C3) (adj C3 B33)
            (adj D4 I56) (adj I56 D4)
            (adj E3 I78) (adj I78 E3)
            (adj F13 I68) (adj I68 F13)
            (adj G7 I28) (adj I28 G7)
            (adj G4 H22) (adj H22 G4)
            (adj H7 I8) (adj I8 H7)
    )
    ; plastic goal example
    (:goal ( or (and (agent_at robot C9) (bin_at bin1 C9) (throw_in_bin bin1) ) (and (agent_at robot E39) (bin_at bin2 E39) (throw_in_bin bin2) ) (and (agent_at robot H12) (bin_at bin3 H12) (throw_in_bin bin3)) ) )
)