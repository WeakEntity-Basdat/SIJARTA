def get_user_query(phone_number):
    return f"""
        SELECT
            m.ID,
            m.Nama,
            m.Email,
            COALESCE(u.ID, p.ID, a.ID) AS Member_ID,
            CASE
                WHEN u.ID IS NOT NULL THEN 'umpire'
                WHEN p.ID IS NOT NULL THEN 'pelatih'
                WHEN a.ID IS NOT NULL THEN 'atlet'
                ELSE 'Unknown'
            END AS Member_Type,
            u.Negara,
            p.Tanggal_Mulai,
            a.Tgl_Lahir,
            a.Negara_Asal,
            a.Play_Right,
            a.Height,
            a.Jenis_Kelamin,
            p.Bank_Name,
            p.Account_Number,
            p.NPWP
        FROM
            MEMBER m
            LEFT JOIN UMPIRE u ON m.ID = u.ID
            LEFT JOIN PELATIH p ON m.ID = p.ID
            LEFT JOIN ATLET a ON m.ID = a.ID
        WHERE
            m.phone_number = '{phone_number}';
    """

def insert_pekerja_query(id, tanggal_mulai, bank_name, account_number, npwp):
    return f"""
        INSERT INTO
        PEKERJA (ID, Tanggal_Mulai, Bank_Name, Account_Number, NPWP)
        VALUES
            (
                '{id}',
                '{tanggal_mulai}',
                '{bank_name}',
                '{account_number}',
                '{npwp}'
            );
    """

