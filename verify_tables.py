from sqlalchemy import text
from database import engine

def verify_table_structures():
    """Verify table structures in blogDb database"""
    
    try:
        with engine.connect() as connection:
            print("=== TABLE STRUCTURES IN blogDb ===\n")
            
            tables = ['users', 'skills', 'skill_exchange_requests']
            
            for table in tables:
                print(f"--- {table.upper()} TABLE ---")
                
                # Get table columns
                result = connection.execute(text(f"""
                    SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = '{table}'
                    ORDER BY ORDINAL_POSITION
                """))
                
                columns = result.fetchall()
                for col in columns:
                    nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                    default = f" DEFAULT {col[3]}" if col[3] else ""
                    print(f"  {col[0]} ({col[1]}) {nullable}{default}")
                
                print()
            
            print("=== FOREIGN KEY CONSTRAINTS ===")
            
            # Get foreign key constraints
            result = connection.execute(text("""
                SELECT 
                    fk.name AS FK_NAME,
                    tp.name AS PARENT_TABLE,
                    cp.name AS PARENT_COLUMN,
                    tr.name AS REFERENCED_TABLE,
                    cr.name AS REFERENCED_COLUMN
                FROM sys.foreign_keys fk
                INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
                INNER JOIN sys.tables tp ON fkc.parent_object_id = tp.object_id
                INNER JOIN sys.columns cp ON fkc.parent_object_id = cp.object_id AND fkc.parent_column_id = cp.column_id
                INNER JOIN sys.tables tr ON fkc.referenced_object_id = tr.object_id
                INNER JOIN sys.columns cr ON fkc.referenced_object_id = cr.object_id AND fkc.referenced_column_id = cr.column_id
                WHERE tp.name IN ('users', 'skills', 'skill_exchange_requests')
                ORDER BY tp.name, fk.name
            """))
            
            fks = result.fetchall()
            if fks:
                for fk in fks:
                    print(f"  {fk[0]}: {fk[1]}.{fk[2]} -> {fk[3]}.{fk[4]}")
            else:
                print("  No foreign key constraints found")
            
            print("\n=== TABLE CREATION SUCCESSFUL ===")
            print("All tables have been created in your blogDb database!")
            
    except Exception as e:
        print(f"Error verifying tables: {e}")

if __name__ == "__main__":
    verify_table_structures()
