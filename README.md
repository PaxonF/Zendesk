# Zendesk
Pull Zendesk ticket's and comments with Python 3.5
These two scripts will allow you too....
	1. pull all zendesk tickets for a date range you desire.
	2. Get all the comments associated with those tickets.

You will need login-id, password and secret API key from the Zendesk website, as well as your specific URL.
You will need a SQL database. HEre are the DDL statements for the simple tables.

CREATE TABLE [dbo].[Tickets](
	[TicketId] [nvarchar](150) NULL,
	[DateInserted] [datetime] NULL,
	[CommentsRetrieved] [bit] NULL
) 
GO

ALTER TABLE [dbo].[Tickets] ADD  DEFAULT (getdate()) FOR [DateInserted]
GO

ALTER TABLE [dbo].[Tickets] ADD  DEFAULT ((0)) FOR [CommentsRetrieved]
GO

CREATE TABLE [dbo].[TicketComments](
	[TicketId] [nvarchar](150) NULL,
	[CommentId] [nvarchar](150) NULL,
	[Comment] [nvarchar](max) NULL,
	[CommentCreate] [nvarchar](150) NULL
) 

GO
