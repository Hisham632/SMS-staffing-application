import 'package:flutter/material.dart';

class ShiftRequest {
  final String position;
  final DateTime date;
  final TimeOfDay fromTime;
  final TimeOfDay toTime;
  final DateTime replyDeadline;

  ShiftRequest({
    required this.position,
    required this.date,
    required this.fromTime,
    required this.toTime,
    required this.replyDeadline,
  });
}
class ShiftRequestsListPage22 extends StatefulWidget {
  final List<ShiftRequest> shiftRequests;

  ShiftRequestsListPage22({Key? key, required this.shiftRequests}) : super(key: key);

  @override
  _ShiftRequestsListPageState createState() => _ShiftRequestsListPageState();
}

class _ShiftRequestsListPageState extends State<ShiftRequestsListPage22> {
  List<ShiftRequest> _shiftRequests=[
    ShiftRequest(
      position: "Cashier",
      date: DateTime(2023, 12, 1),
      fromTime: TimeOfDay(hour: 9, minute: 0),
      toTime: TimeOfDay(hour: 17, minute: 0),
      replyDeadline: DateTime(2023, 11, 25),
    ),
    ShiftRequest(
      position: "Barista",
      date: DateTime(2023, 12, 2),
      fromTime: TimeOfDay(hour: 8, minute: 0),
      toTime: TimeOfDay(hour: 16, minute: 0),
      replyDeadline: DateTime(2023, 11, 26),
    ),
    ShiftRequest(
      position: "Barista",
      date: DateTime(2023, 12, 2),
      fromTime: TimeOfDay(hour: 8, minute: 0),
      toTime: TimeOfDay(hour: 16, minute: 0),
      replyDeadline: DateTime(2023, 11, 26),
    ),      ShiftRequest(
      position: "Barista",
      date: DateTime(2023, 12, 2),
      fromTime: TimeOfDay(hour: 8, minute: 0),
      toTime: TimeOfDay(hour: 16, minute: 0),
      replyDeadline: DateTime(2023, 11, 26),
    ),      ShiftRequest(
      position: "Barista",
      date: DateTime(2023, 12, 2),
      fromTime: TimeOfDay(hour: 8, minute: 0),
      toTime: TimeOfDay(hour: 16, minute: 0),
      replyDeadline: DateTime(2023, 11, 26),
    ),      ShiftRequest(
      position: "Barista",
      date: DateTime(2023, 12, 2),
      fromTime: TimeOfDay(hour: 8, minute: 0),
      toTime: TimeOfDay(hour: 16, minute: 0),
      replyDeadline: DateTime(2023, 11, 26),
    ),
    // Add more objects as needed
  ];

  @override
  void initState() {
    super.initState();
    // _shiftRequests = widget.shiftRequests;
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[850], // Dark background like CreateShiftRequestPage33
      appBar: AppBar(
        title: Text(
          'Open Shift Requests',
          style: TextStyle(
            color: Colors.white,
            fontSize: 20,
            fontWeight: FontWeight.bold,
            fontFamily: 'Roboto', // Consistent font family
          ),
        ),
        backgroundColor: Colors.grey[900], // Consistent AppBar color
        centerTitle: true,
      ),
      body: ListView.builder(
        itemCount: _shiftRequests.length,
        itemBuilder: (context, index) {
          return _buildShiftRequestItem(context, _shiftRequests[index]);
        },
      ),
    );
  }

  Widget _buildShiftRequestItem(BuildContext context, ShiftRequest request) {
    return Container(
      margin: EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(15),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.2),
            spreadRadius: 3,
            blurRadius: 5,
            offset: Offset(0, 3),
          ),
        ],
      ),
      child: ListTile(
        contentPadding: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
        title: Text(
          request.position,
          style: TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 18,
            fontFamily: 'Roboto', // Consistent font family
            color: Colors.black, // Text color
          ),
        ),
        subtitle: Padding(
          padding: EdgeInsets.only(top: 8),
          child: Text(
            _formatShiftDetails(request),
            textAlign: TextAlign.left,
            style: TextStyle(
              fontSize: 14,
              color: Colors.black,
              fontWeight: FontWeight.bold,
              fontFamily: 'Proxima Nova',
            ),
            overflow: TextOverflow.ellipsis,
          ),
        ),
        trailing: IconButton(
          icon: Icon(Icons.cancel, color: Colors.red),
          onPressed: () => _showCancelConfirmation(context, request),
        ),
        onTap: () {
          // Handle tap event
        },
      ),
    );
  }


  String _formatShiftDetails(ShiftRequest request) {
    String formatDate(DateTime date) {
      return '${date.year}-${date.month.toString().padLeft(2, '0')}-${date.day.toString().padLeft(2, '0')}';
    }

    String formatTime(TimeOfDay time) {
      final hour = time.hour.toString().padLeft(2, '0');
      final minute = time.minute.toString().padLeft(2, '0');
      return '$hour:$minute';
    }

    return 'Date: ${formatDate(request.date)}, '
        'From: ${formatTime(request.fromTime)} '
        'to ${formatTime(request.toTime)}\n'
        'Reply by: ${formatDate(request.replyDeadline)}';
  }


  void _showCancelConfirmation(BuildContext context, ShiftRequest request) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Cancel Request'),
        content: Text('Are you sure you want to cancel this shift request for ${request.position}?'),
        actions: <Widget>[
          TextButton(
            onPressed: () {
              setState(() {
                _shiftRequests.remove(request);
              });
              Navigator.of(context).pop(); // Close the dialog
            },
            child: Text('Yes', style: TextStyle(color: Colors.red)),
          ),
          TextButton(
            onPressed: () {
              Navigator.of(context).pop(); // Close the dialog without removing
            },
            child: Text('No'),
          ),
        ],
      ),
    );
  }
}
