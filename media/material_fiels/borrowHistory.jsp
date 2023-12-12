<%@ page import="java.sql.Connection" %>
<%@ page import="java.sql.DriverManager" %>
<%@ page import="java.sql.PreparedStatement" %>
<%@ page import="java.sql.ResultSet" %>
<%@ page import="java.sql.SQLException" %>
<%@ page import="jakarta.servlet.ServletException" %>
<%@ page import="jakarta.servlet.annotation.WebServlet" %>
<%@ page import="jakarta.servlet.http.HttpServlet" %>
<%@ page import="jakarta.servlet.http.HttpServletRequest" %>
<%@ page import="jakarta.servlet.http.HttpServletResponse" %>
<%@ page import="jakarta.servlet.RequestDispatcher" %>
<%@ page import="jakarta.servlet.http.HttpSession" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.text.SimpleDateFormat" %>

<html>
<head>
    <title>Booking History</title>
     <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }

        header {
            background-color: #333;
            color: #fff;
            text-align: center;
            padding: 1em;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }

        th {
            background-color: #4CAF50;
            color: white;
        }

        tr:nth-child(even) {
            background-color: #f2f2f2;
        }

        tr:hover {
            background-color: #ddd;
        }
        caption {
            caption-side: top;
            font-weight: bold;
            font-size: 1.2em;
            margin-bottom: 10px;
        }
    </style>
        <link rel="stylesheet" href="css/add.css">
    
</head>
<body>
<nav>
    <ul>
        <li><a class="nav-link" href="index.jsp">Home</a></li>
        <li><a class="nav-link" href="#">Contact</a></li>
    </ul>
    <div class="user-actions">
        
        <a class="logout" href="LogoutServlet">Logout</a>
    </div>
</nav>
<%

String userName = (String) session.getAttribute("name");
Integer userIdObj = (Integer) session.getAttribute("userId");

// Check if userIdObj is not null before converting to int
int userId = (userIdObj != null) ? userIdObj.intValue() : 0;

    // Database connection details
    String jdbcUrl = "jdbc:mysql://localhost:3306/projet";
    String dbUser = "root";
    String dbPassword = "hamdi";

    Connection connection = null;
    PreparedStatement preparedStatement = null;
    ResultSet resultSet = null;

    try {
        Class.forName("com.mysql.cj.jdbc.Driver");
        connection = DriverManager.getConnection(jdbcUrl, dbUser, dbPassword);
        String query = "SELECT e.id, e.date_emprunt, e.date_retour, e.livre_id, " +
                "l.titre, l.auteur, l.genre " +
                "FROM Emprunt e " +
                "JOIN Livres l ON e.livre_id = l.id " +
                "WHERE e.utilisateur_id = ?";

        preparedStatement = connection.prepareStatement(query);
        preparedStatement.setInt(1, userId);

        resultSet = preparedStatement.executeQuery();
    %>
    <table border="1">
    <caption>Booking History Details</caption>
        <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Author</th>
            <th>Borrow Date</th>
            <th>Return Date</th>
            <th>Status</th>
        </tr>
        <%
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");

            while (resultSet.next()) {
                int id = resultSet.getInt("id");
                String title = resultSet.getString("titre");
                String author = resultSet.getString("auteur");
                String returnDateStr = resultSet.getString("date_retour");
                String borrowDateStr = resultSet.getString("date_emprunt");

                java.util.Date returnDate = dateFormat.parse(returnDateStr);
                java.util.Date currentDate = new java.util.Date();

                String status = (currentDate.after(returnDate)) ? "Returned" : "Still borrowed";
        %>
        <tr>
            <td><%= id %></td>
            <td><%= title %></td>
            <td><%= author %></td>
            <td><%= borrowDateStr %></td>
            <td><%= returnDateStr %></td>
            <td><%= status %></td>
        </tr>
        <%
            }
        %>
    </table>
    <%
    } catch (ClassNotFoundException | SQLException e) {
        e.printStackTrace(); // Handle this exception properly in your application
    } finally {
        // Close resources in the finally block
        try {
            if (resultSet != null) {
                resultSet.close();
            }
            if (preparedStatement != null) {
                preparedStatement.close();
            }
            if (connection != null) {
                connection.close();
            }
        } catch (SQLException e) {
            e.printStackTrace(); // Handle this exception properly in your application
        }
    }
%>

</body>
</html>
