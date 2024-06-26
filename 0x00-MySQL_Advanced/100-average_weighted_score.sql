-- Create stored procedure ComputeAverageWeightedScoreForUser
-- computes and stores the average weighted score for a student
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
BEGIN
        SET @average := (SELECT
            SUM(corrections.score * projects.weight) / SUM(projects.weight)
            FROM corrections
            INNER JOIN projects
            ON projects.id = corrections.project_id
            WHERE corrections.user_id = user_id);
        UPDATE users SET average_score = @average WHERE users.id = user_id; 
END //

DELIMITER ;
