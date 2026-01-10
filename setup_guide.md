# Database Setup Guide for Community Skill Swap Platform

## Quick Setup Options

### Option 1: SQLite (Easiest for Testing)
Perfect for development and testing without SQL Server setup.

1. **Update database.py to use SQLite:**
   ```python
   # In database.py, change the database_url to:
   database_url: str = "sqlite:///./skill_swap.db"
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```
   Tables will be created automatically in a local SQLite file.

### Option 2: SQL Server (Production Ready)
Follow these steps to set up SQL Server properly.

## SQL Server Setup Steps

### 1. Install SQL Server
- **SQL Server Express** (Free): https://www.microsoft.com/sql-server/sql-server-downloads
- Choose "Express" or "Developer" edition
- During installation, note:
  - Instance name (usually SQLEXPRESS)
  - SA password
  - Enable mixed authentication (SQL Server + Windows)

### 2. Enable SQL Server Configuration
1. Open **SQL Server Configuration Manager**
2. Go to **SQL Server Network Configuration** → **Protocols for SQLEXPRESS**
3. Enable **TCP/IP**
4. Right-click TCP/IP → Properties → IP Addresses tab
5. Scroll to IPAll, set **TCP Port** to **1433**
6. Restart SQL Server service

### 3. Configure Firewall
1. Open Windows Firewall
2. Add inbound rule for port 1433
3. Allow SQL Server (TCP 1433)

### 4. Test Connection
Open **SQL Server Management Studio** and connect with:
- Server name: `localhost\SQLEXPRESS` or `localhost,1433`
- Authentication: SQL Server Authentication
- Login: `sa`
- Password: [your SA password]

### 5. Update Database Connection
Create `.env` file:
```
DATABASE_URL=mssql+pyodbc://sa:YourPassword@localhost/SQLEXPRESS?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes
```

Or update `database.py` directly:
```python
database_url: str = "mssql+pyodbc://sa:YourPassword@localhost/SQLEXPRESS?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
```

### 6. Install Required Driver
Ensure ODBC Driver 17 is installed:
https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server

### 7. Run Database Initialization
```bash
python init_database.py
```

## Common Issues & Solutions

### Issue: "Named Pipes Provider: Could not open a connection"
**Solution:**
1. Check SQL Server service is running
2. Enable TCP/IP in SQL Server Configuration Manager
3. Check firewall settings
4. Verify server name and port

### Issue: "Login failed for user 'sa'"
**Solution:**
1. Enable SA account in SQL Server Management Studio
2. Check SA password is correct
3. Enable mixed authentication

### Issue: "ODBC Driver not found"
**Solution:**
1. Install ODBC Driver 17 for SQL Server
2. Restart your computer after installation

### Issue: "TrustServerCertificate error"
**Solution:**
Add `TrustServerCertificate=yes` to connection string

## Testing Your Setup

### 1. Test Database Connection
```bash
python -c "from database import engine; print('Database connected!' if engine else 'Failed')"
```

### 2. Run Application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Check Database Status
Open: http://localhost:8000/database-status

### 4. View API Documentation
Open: http://localhost:8000/docs

## Alternative: Docker SQL Server
If you have Docker, you can quickly set up SQL Server:

```bash
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=YourStrongPassword123" \
   -p 1433:1433 --name sql_server \
   -m 2g -d mcr.microsoft.com/mssql/server:2019-latest
```

Then use connection string:
```
DATABASE_URL=mssql+pyodbc://sa:YourStrongPassword123@localhost:1433/master?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes
```

## Production Considerations

1. **Security:**
   - Use strong passwords
   - Enable SSL/TLS
   - Limit database user permissions

2. **Performance:**
   - Add database indexes
   - Configure connection pooling
   - Monitor query performance

3. **Backup:**
   - Set up regular database backups
   - Test restore procedures

## Need Help?

If you're still having issues:
1. Check SQL Server logs
2. Verify network connectivity
3. Test with SQL Server Management Studio first
4. Try SQLite option for initial development
